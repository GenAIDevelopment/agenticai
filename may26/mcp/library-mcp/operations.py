"""
Library operations — SQL-backed business logic for the library MCP server.

Every function here talks to MySQL through the helpers in `db.py`:
  * execute_query        -> single statement (SELECT returns rows; writes commit)
  * execute_transaction  -> several statements in one atomic transaction

IDs: callers may pass either a numeric users.user_id / book_copies.book_id, or a
human code such as 'STU001' (users.user_code) or 'EMP001' (librarians.employee_no).
The small `_resolve_*` helpers normalise those to the numeric keys the tables use.

Schema reference: data/01_library_schema.sql
"""

from datetime import datetime

from db import execute_query, execute_transaction

# --- Library policy constants (tweak to match your college rules) ----------
LOAN_PERIOD_DAYS = 14          # default borrowing window
FINE_PER_DAY = 5.00            # late-return fine per day overdue
FINE_GRACE_DAYS = 30           # days a student has to pay an assessed fine
DEFAULT_LIBRARIAN = "EMP001"   # librarian on duty when none is supplied


# ===========================================================================
# Helpers
# ===========================================================================
def _resolve_user_id(student_id) -> int:
    """Return users.user_id for a numeric id or a user_code like 'STU001'."""
    if isinstance(student_id, int) or str(student_id).isdigit():
        return int(student_id)
    rows = execute_query(
        "SELECT user_id FROM users WHERE user_code = %s", (student_id,)
    )
    if not rows:
        raise ValueError(f"No user found with code {student_id!r}")
    return rows[0][0]


def _resolve_librarian_id(librarian) -> int:
    """Return librarians.librarian_id for a numeric id or an employee_no like 'EMP001'."""
    if isinstance(librarian, int) or str(librarian).isdigit():
        return int(librarian)
    rows = execute_query(
        "SELECT librarian_id FROM librarians WHERE employee_no = %s", (librarian,)
    )
    if not rows:
        raise ValueError(f"No librarian found with employee_no {librarian!r}")
    return rows[0][0]


def _quarter_range(year: int, quarter: int) -> tuple[str, str]:
    """Return [start, end) date strings for a calendar quarter (1-4)."""
    if quarter not in (1, 2, 3, 4):
        raise ValueError("quarter must be 1, 2, 3 or 4")
    start_month = 3 * (quarter - 1) + 1
    end_month = start_month + 3
    end_year = year + (1 if end_month > 12 else 0)
    end_month = end_month - 12 if end_month > 12 else end_month
    return f"{year}-{start_month:02d}-01", f"{end_year}-{end_month:02d}-01"


# ===========================================================================
# Circulation: issue / return / pending returns
# ===========================================================================
def issue_book(
    student_id,
    book_id: int,
    date: str,
    librarian=DEFAULT_LIBRARIAN,
    loan_days: int = LOAN_PERIOD_DAYS,
) -> str:
    """Issue an available copy of `book_id` to a student, due `loan_days` later."""
    user_id = _resolve_user_id(student_id)
    lib_id = _resolve_librarian_id(librarian)

    copies = execute_query(
        "SELECT copy_id FROM book_copies "
        "WHERE book_id = %s AND status = 'AVAILABLE' LIMIT 1",
        (book_id,),
    )
    if not copies:
        return f"No available copies for book {book_id}."
    copy_id = copies[0][0]

    steps = [
        (
            """INSERT INTO loan_transactions
                 (copy_id, borrower_user_id, issued_by_librarian_id,
                  issued_at, due_at, status)
               VALUES (%s, %s, %s, %s, DATE_ADD(%s, INTERVAL %s DAY), 'ISSUED')""",
            (copy_id, user_id, lib_id, date, date, loan_days),
        ),
        ("UPDATE book_copies SET status = 'ISSUED' WHERE copy_id = %s", (copy_id,)),
        (
            "UPDATE books SET available_copies = available_copies - 1 "
            "WHERE book_id = %s AND available_copies > 0",
            (book_id,),
        ),
        (
            """INSERT INTO book_ledger_entries
                 (book_id, copy_id, loan_id, entry_type, entry_date, quantity)
               VALUES (%s, %s, LAST_INSERT_ID(), 'ISSUE', %s, 1)""",
            (book_id, copy_id, date),
        ),
    ]
    loan_id = execute_transaction(steps)[0]
    return (
        f"Issued copy {copy_id} of book {book_id} to {student_id} "
        f"(loan #{loan_id}); due in {loan_days} days."
    )


def process_return(
    student_id,
    book_id: int,
    date: str,
    description: str = "",
    librarian=DEFAULT_LIBRARIAN,
    fine_per_day: float = FINE_PER_DAY,
) -> float:
    """
    Return a borrowed book. Marks the loan returned, frees the copy, logs the
    ledger entry, and — if overdue — assesses a late fine. Returns the fine
    amount (0.0 when on time).
    """
    user_id = _resolve_user_id(student_id)
    lib_id = _resolve_librarian_id(librarian)

    loans = execute_query(
        """SELECT l.loan_id, l.copy_id, l.due_at
             FROM loan_transactions l
             JOIN book_copies c ON c.copy_id = l.copy_id
            WHERE l.borrower_user_id = %s AND c.book_id = %s
              AND l.status IN ('ISSUED', 'OVERDUE')
            ORDER BY l.issued_at ASC
            LIMIT 1""",
        (user_id, book_id),
    )
    if not loans:
        raise ValueError(
            f"No active loan found for user {student_id} and book {book_id}"
        )
    loan_id, copy_id, due_at = loans[0]

    overdue_days = execute_query(
        "SELECT GREATEST(0, DATEDIFF(%s, %s))", (date, due_at)
    )[0][0]
    fine_amount = float(overdue_days) * fine_per_day

    steps = [
        (
            """UPDATE loan_transactions
                  SET status = 'RETURNED', returned_at = %s,
                      returned_by_librarian_id = %s
                WHERE loan_id = %s""",
            (date, lib_id, loan_id),
        ),
        ("UPDATE book_copies SET status = 'AVAILABLE' WHERE copy_id = %s", (copy_id,)),
        (
            "UPDATE books SET available_copies = available_copies + 1 "
            "WHERE book_id = %s",
            (book_id,),
        ),
        (
            """INSERT INTO book_ledger_entries
                 (book_id, copy_id, loan_id, entry_type, entry_date, quantity)
               VALUES (%s, %s, %s, 'RETURN', %s, 1)""",
            (book_id, copy_id, loan_id, date),
        ),
    ]

    if fine_amount > 0:
        steps.append(
            (
                """INSERT INTO fines
                     (loan_id, user_id, fine_type, assessed_at, due_date,
                      amount, status, remarks)
                   VALUES (%s, %s, 'LATE_RETURN', %s,
                           DATE_ADD(%s, INTERVAL %s DAY), %s, 'UNPAID', %s)""",
                (
                    loan_id,
                    user_id,
                    date,
                    date,
                    FINE_GRACE_DAYS,
                    fine_amount,
                    description or f"{overdue_days} day(s) overdue",
                ),
            )
        )
        steps.append(_upsert_fine_assessed(user_id, fine_amount))

    execute_transaction(steps)
    return fine_amount


def get_pending_returns():
    """All books currently out on loan (issued or overdue), oldest due first."""
    return execute_query(
        """SELECT l.loan_id, u.user_code,
                  CONCAT(u.first_name, ' ', u.last_name) AS borrower,
                  b.title, c.barcode, l.issued_at, l.due_at,
                  GREATEST(0, DATEDIFF(NOW(), l.due_at)) AS overdue_days
             FROM loan_transactions l
             JOIN users u       ON u.user_id = l.borrower_user_id
             JOIN book_copies c ON c.copy_id = l.copy_id
             JOIN books b       ON b.book_id = c.book_id
            WHERE l.status IN ('ISSUED', 'OVERDUE')
            ORDER BY l.due_at ASC"""
    )


def get_returns_due_today(date: str | None = None):
    """Loans whose due date is `date` (defaults to today). Used for reminders."""
    if date is None:
        return execute_query(
            """SELECT l.loan_id, u.user_code, u.email,
                      CONCAT(u.first_name, ' ', u.last_name) AS borrower,
                      b.title, c.barcode, l.due_at
                 FROM loan_transactions l
                 JOIN users u       ON u.user_id = l.borrower_user_id
                 JOIN book_copies c ON c.copy_id = l.copy_id
                 JOIN books b       ON b.book_id = c.book_id
                WHERE l.status IN ('ISSUED', 'OVERDUE')
                  AND DATE(l.due_at) = CURDATE()
                ORDER BY u.user_code"""
        )
    return execute_query(
        """SELECT l.loan_id, u.user_code, u.email,
                  CONCAT(u.first_name, ' ', u.last_name) AS borrower,
                  b.title, c.barcode, l.due_at
             FROM loan_transactions l
             JOIN users u       ON u.user_id = l.borrower_user_id
             JOIN book_copies c ON c.copy_id = l.copy_id
             JOIN books b       ON b.book_id = c.book_id
            WHERE l.status IN ('ISSUED', 'OVERDUE')
              AND DATE(l.due_at) = %s
            ORDER BY u.user_code""",
        (date,),
    )


def mark_overdue_loans(date: str | None = None) -> int:
    """Flip ISSUED loans past their due date to OVERDUE. Returns rows touched."""
    if date is None:
        execute_query(
            "UPDATE loan_transactions SET status = 'OVERDUE' "
            "WHERE status = 'ISSUED' AND due_at < NOW()"
        )
    else:
        execute_query(
            "UPDATE loan_transactions SET status = 'OVERDUE' "
            "WHERE status = 'ISSUED' AND due_at < %s",
            (date,),
        )
    # execute_query does not surface rowcount; report count via a follow-up read
    return get_overdue_count()


def get_overdue_count() -> int:
    rows = execute_query(
        "SELECT COUNT(*) FROM loan_transactions WHERE status = 'OVERDUE'"
    )
    return int(rows[0][0])


# ===========================================================================
# Fine management
# ===========================================================================
def _upsert_fine_assessed(user_id: int, amount: float):
    """Transaction step: add an assessed fine to the user's account balance."""
    return (
        """INSERT INTO user_accounts (user_id, total_fines_assessed, current_balance)
           VALUES (%s, %s, %s)
           ON DUPLICATE KEY UPDATE
             total_fines_assessed = total_fines_assessed + %s,
             current_balance      = current_balance + %s""",
        (user_id, amount, amount, amount, amount),
    )


def get_fine_due(student_id) -> float:
    """Total unpaid fine balance (amount - amount_paid) for a student."""
    user_id = _resolve_user_id(student_id)
    rows = execute_query(
        """SELECT COALESCE(SUM(amount - amount_paid), 0)
             FROM fines
            WHERE user_id = %s AND status IN ('UNPAID', 'PARTIALLY_PAID')""",
        (user_id,),
    )
    return float(rows[0][0])


def collect_fine(
    student_id,
    amount: float,
    method: str = "CASH",
    librarian=DEFAULT_LIBRARIAN,
    date: str | None = None,
) -> float:
    """
    Collect a payment and apply it to the student's oldest outstanding fines
    first. Records fine_payments, updates fine status, the library ledger, and
    the user's account balance. Returns the amount actually applied.
    """
    user_id = _resolve_user_id(student_id)
    lib_id = _resolve_librarian_id(librarian)
    paid_at = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    outstanding = execute_query(
        """SELECT fine_id, amount, amount_paid
             FROM fines
            WHERE user_id = %s AND status IN ('UNPAID', 'PARTIALLY_PAID')
            ORDER BY assessed_at ASC""",
        (user_id,),
    )

    remaining = float(amount)
    applied = 0.0
    steps: list[tuple[str, tuple]] = []

    for fine_id, fine_amount, amount_paid in outstanding:
        if remaining <= 0:
            break
        due = float(fine_amount) - float(amount_paid)
        pay = min(due, remaining)
        new_paid = float(amount_paid) + pay
        new_status = "PAID" if new_paid >= float(fine_amount) else "PARTIALLY_PAID"

        steps.append(
            (
                """INSERT INTO fine_payments
                     (fine_id, paid_at, amount, payment_method, received_by_librarian_id)
                   VALUES (%s, %s, %s, %s, %s)""",
                (fine_id, paid_at, pay, method, lib_id),
            )
        )
        steps.append(
            (
                "UPDATE fines SET amount_paid = %s, status = %s WHERE fine_id = %s",
                (new_paid, new_status, fine_id),
            )
        )
        steps.append(
            (
                """INSERT INTO library_account_ledger
                     (entry_date, entry_type, amount, reference_table,
                      reference_id, description)
                   VALUES (%s, 'FINE_COLLECTED', %s, 'fines', %s, %s)""",
                (paid_at, pay, fine_id, f"Fine payment from {student_id}"),
            )
        )
        remaining -= pay
        applied += pay

    if applied > 0:
        steps.append(
            (
                """INSERT INTO user_accounts
                     (user_id, total_payments_received, current_balance)
                   VALUES (%s, %s, 0)
                   ON DUPLICATE KEY UPDATE
                     total_payments_received = total_payments_received + %s,
                     current_balance         = current_balance - %s""",
                (user_id, applied, applied, applied),
            )
        )
        execute_transaction(steps)

    return applied


def get_outstanding_fines():
    """Every user with money owed, biggest balance first (fine management view)."""
    return execute_query(
        """SELECT u.user_id, u.user_code,
                  CONCAT(u.first_name, ' ', u.last_name) AS user_name,
                  ua.total_fines_assessed, ua.total_payments_received,
                  ua.current_balance
             FROM user_accounts ua
             JOIN users u ON u.user_id = ua.user_id
            WHERE ua.current_balance > 0
            ORDER BY ua.current_balance DESC"""
    )


# ===========================================================================
# Account balances & statements
# ===========================================================================
def total_account_balance(student_id) -> float:
    """Current outstanding balance on a student's library account."""
    user_id = _resolve_user_id(student_id)
    rows = execute_query(
        "SELECT current_balance FROM user_accounts WHERE user_id = %s", (user_id,)
    )
    return float(rows[0][0]) if rows else 0.0


def get_account_summary(student_id):
    """Full account snapshot for a student (one row from user_accounts)."""
    user_id = _resolve_user_id(student_id)
    return execute_query(
        """SELECT u.user_code,
                  CONCAT(u.first_name, ' ', u.last_name) AS user_name,
                  ua.opening_balance, ua.total_fines_assessed,
                  ua.total_payments_received, ua.total_waived,
                  ua.current_balance, ua.last_updated
             FROM user_accounts ua
             JOIN users u ON u.user_id = ua.user_id
            WHERE ua.user_id = %s""",
        (user_id,),
    )


def create_account_statement(from_date: str, to_date: str):
    """
    Library-wide financial statement between two dates: every ledger movement
    plus totals grouped by entry type.
    """
    entries = execute_query(
        """SELECT entry_date, entry_type, amount, reference_table,
                  reference_id, description
             FROM library_account_ledger
            WHERE entry_date >= %s AND entry_date < %s
            ORDER BY entry_date ASC""",
        (from_date, to_date),
    )
    totals = execute_query(
        """SELECT entry_type, COUNT(*) AS entries, SUM(amount) AS total
             FROM library_account_ledger
            WHERE entry_date >= %s AND entry_date < %s
            GROUP BY entry_type
            ORDER BY entry_type""",
        (from_date, to_date),
    )
    return {"from": from_date, "to": to_date, "entries": entries, "totals": totals}


# ===========================================================================
# No-dues certificate
# ===========================================================================
def issue_no_due_certificate(student_id) -> dict:
    """
    Check a student is clear of dues. A certificate is granted only when there
    are no outstanding fines and no books still on loan.
    """
    user_id = _resolve_user_id(student_id)
    fine_due = get_fine_due(student_id)
    active = execute_query(
        """SELECT COUNT(*) FROM loan_transactions
            WHERE borrower_user_id = %s AND status IN ('ISSUED', 'OVERDUE')""",
        (user_id,),
    )[0][0]

    cleared = fine_due <= 0 and active == 0
    return {
        "student_id": student_id,
        "fine_due": fine_due,
        "books_on_loan": int(active),
        "no_dues": cleared,
        "issued_on": datetime.now().strftime("%Y-%m-%d") if cleared else None,
        "message": (
            "No-dues certificate issued."
            if cleared
            else f"Cannot issue: ₹{fine_due:.2f} due, {active} book(s) not returned."
        ),
    }


# ===========================================================================
# Catalog & book master data
# ===========================================================================
def add_book(
    title: str,
    isbn13: str | None = None,
    subject: str | None = None,
    publisher_id: int | None = None,
    publication_year: int | None = None,
    copies: int = 1,
    price: float | None = None,
    call_number: str | None = None,
    shelf_location: str | None = None,
    date: str | None = None,
) -> int:
    """
    Add a new title to the catalog and create its physical copies (each with an
    ACQUISITION ledger entry). Returns the new book_id.
    """
    acquired = date or datetime.now().strftime("%Y-%m-%d")
    book_id = execute_transaction(
        [
            (
                """INSERT INTO books
                     (isbn13, title, subject, publisher_id, publication_year,
                      call_number, shelf_location, total_copies, available_copies)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, 0, 0)""",
                (
                    isbn13,
                    title,
                    subject,
                    publisher_id,
                    publication_year,
                    call_number,
                    shelf_location,
                ),
            )
        ]
    )[0]
    add_copies(book_id, copies, price=price, date=acquired)
    return book_id


def add_copies(
    book_id: int,
    count: int = 1,
    price: float | None = None,
    condition: str = "NEW",
    date: str | None = None,
) -> list[int]:
    """Add `count` copies to an existing book and log each as an ACQUISITION."""
    acquired = date or datetime.now().strftime("%Y-%m-%d")
    existing = execute_query(
        "SELECT COUNT(*) FROM book_copies WHERE book_id = %s", (book_id,)
    )[0][0]

    copy_ids: list[int] = []
    for i in range(count):
        seq = existing + i + 1
        barcode = f"BC-{book_id}-{seq:04d}"
        accession = f"ACC-{book_id}-{seq:04d}"
        copy_id = execute_transaction(
            [
                (
                    """INSERT INTO book_copies
                         (book_id, barcode, accession_no, status,
                          condition_status, acquired_date, purchase_price)
                       VALUES (%s, %s, %s, 'AVAILABLE', %s, %s, %s)""",
                    (book_id, barcode, accession, condition, acquired, price),
                ),
                (
                    """INSERT INTO book_ledger_entries
                         (book_id, copy_id, entry_type, entry_date, quantity, notes)
                       VALUES (%s, LAST_INSERT_ID(), 'ACQUISITION', %s, 1,
                               'New copy acquired')""",
                    (book_id, acquired),
                ),
            ]
        )[0]
        copy_ids.append(copy_id)

    execute_query(
        """UPDATE books
              SET total_copies     = total_copies + %s,
                  available_copies = available_copies + %s
            WHERE book_id = %s""",
        (count, count, book_id),
    )
    return copy_ids


def retire_book(book_id: int, date: str | None = None,
                notes: str = "Retired from circulation") -> str:
    """
    Withdraw a book from circulation: deactivate the title, mark its available
    copies WITHDRAWN, and record a single WITHDRAWAL ledger entry.
    """
    when = date or datetime.now().strftime("%Y-%m-%d")
    withdrawn = execute_query(
        "SELECT COUNT(*) FROM book_copies "
        "WHERE book_id = %s AND status = 'AVAILABLE'",
        (book_id,),
    )[0][0]

    execute_transaction(
        [
            ("UPDATE books SET active = FALSE WHERE book_id = %s", (book_id,)),
            (
                "UPDATE book_copies SET status = 'WITHDRAWN' "
                "WHERE book_id = %s AND status = 'AVAILABLE'",
                (book_id,),
            ),
            (
                "UPDATE books SET available_copies = 0 WHERE book_id = %s",
                (book_id,),
            ),
            (
                """INSERT INTO book_ledger_entries
                     (book_id, entry_type, entry_date, quantity, notes)
                   VALUES (%s, 'WITHDRAWAL', %s, %s, %s)""",
                (book_id, when, withdrawn, notes),
            ),
        ]
    )
    return f"Retired book {book_id}; {withdrawn} copy/copies withdrawn."


def get_book_catalog(active_only: bool = True):
    """Browse the catalog with author names and live copy counts."""
    where = "WHERE b.active = TRUE" if active_only else ""
    return execute_query(
        f"""SELECT b.book_id, b.isbn13, b.title, b.subject,
                   GROUP_CONCAT(DISTINCT a.author_name SEPARATOR ', ') AS authors,
                   b.total_copies, b.available_copies, b.shelf_location
              FROM books b
              LEFT JOIN book_authors ba ON ba.book_id = b.book_id
              LEFT JOIN authors a       ON a.author_id = ba.author_id
              {where}
             GROUP BY b.book_id, b.isbn13, b.title, b.subject,
                      b.total_copies, b.available_copies, b.shelf_location
             ORDER BY b.title ASC"""
    )


def search_book(query: str):
    """Search the catalog by title, subject, ISBN or author name."""
    like = f"%{query}%"
    return execute_query(
        """SELECT DISTINCT b.book_id, b.title, b.subject,
                  b.available_copies, b.total_copies
             FROM books b
             LEFT JOIN book_authors ba ON ba.book_id = b.book_id
             LEFT JOIN authors a       ON a.author_id = ba.author_id
            WHERE b.title LIKE %s OR b.subject LIKE %s
               OR b.isbn13 LIKE %s OR a.author_name LIKE %s
            ORDER BY b.title ASC""",
        (like, like, like, like),
    )


# ===========================================================================
# Resources (read-only lookups)
# ===========================================================================
def book_info_by_id(book_id: int):
    """Full detail for one book including authors and publisher."""
    return execute_query(
        """SELECT b.book_id, b.isbn13, b.title, b.subtitle, b.subject,
                  b.publication_year, p.publisher_name,
                  GROUP_CONCAT(DISTINCT a.author_name SEPARATOR ', ') AS authors,
                  b.total_copies, b.available_copies,
                  b.call_number, b.shelf_location, b.active
             FROM books b
             LEFT JOIN publishers p    ON p.publisher_id = b.publisher_id
             LEFT JOIN book_authors ba ON ba.book_id = b.book_id
             LEFT JOIN authors a       ON a.author_id = ba.author_id
            WHERE b.book_id = %s
            GROUP BY b.book_id, b.isbn13, b.title, b.subtitle, b.subject,
                     b.publication_year, p.publisher_name,
                     b.total_copies, b.available_copies,
                     b.call_number, b.shelf_location, b.active""",
        (book_id,),
    )


def get_book_id(title: str):
    """Resolve a (partial) title to matching book_ids."""
    return execute_query(
        "SELECT book_id, title FROM books WHERE title LIKE %s ORDER BY title",
        (f"%{title}%",),
    )


def get_availability_by_id(book_id: int) -> dict:
    """Available vs total copies for a book."""
    rows = execute_query(
        "SELECT title, available_copies, total_copies FROM books WHERE book_id = %s",
        (book_id,),
    )
    if not rows:
        raise ValueError(f"No book with id {book_id}")
    title, available, total = rows[0]
    return {
        "book_id": book_id,
        "title": title,
        "available_copies": int(available),
        "total_copies": int(total),
        "available": int(available) > 0,
    }


def get_book_rack(book_id: int):
    """Shelf / rack location and call number for a book (rack management)."""
    return execute_query(
        "SELECT book_id, title, call_number, shelf_location "
        "FROM books WHERE book_id = %s",
        (book_id,),
    )


def update_book_rack(book_id: int, call_number: str | None = None,
                     shelf_location: str | None = None) -> str:
    """Update where a book lives on the shelves (rack management)."""
    execute_query(
        """UPDATE books
              SET call_number    = COALESCE(%s, call_number),
                  shelf_location = COALESCE(%s, shelf_location)
            WHERE book_id = %s""",
        (call_number, shelf_location, book_id),
    )
    return f"Updated rack location for book {book_id}."


# ===========================================================================
# Reservations  (per-student queue, backed by the `reservations` table)
# ===========================================================================
def reserve_book(student_id, book_id: int, date: str | None = None,
                 expiry_days: int = 3) -> int:
    """Add a student to the reservation queue for a book. Returns reservation_id."""
    user_id = _resolve_user_id(student_id)
    when = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return execute_transaction(
        [
            (
                """INSERT INTO reservations
                     (book_id, user_id, reserved_at, status, expires_at)
                   VALUES (%s, %s, %s, 'PENDING', DATE_ADD(%s, INTERVAL %s DAY))""",
                (book_id, user_id, when, when, expiry_days),
            )
        ]
    )[0]


def cancel_reservation(reservation_id: int) -> str:
    """Cancel a reservation."""
    execute_query(
        "UPDATE reservations SET status = 'CANCELLED' WHERE reservation_id = %s",
        (reservation_id,),
    )
    return f"Reservation {reservation_id} cancelled."


def fulfill_reservation(reservation_id: int, loan_id: int | None = None) -> str:
    """Mark a reservation fulfilled, optionally linking the loan that satisfied it."""
    execute_query(
        """UPDATE reservations
              SET status = 'FULFILLED', fulfilled_loan_id = %s
            WHERE reservation_id = %s""",
        (loan_id, reservation_id),
    )
    return f"Reservation {reservation_id} fulfilled."


def get_reservation_details_for_book(book_id: int):
    """The active reservation queue for a book, earliest request first."""
    return execute_query(
        """SELECT r.reservation_id, u.user_code,
                  CONCAT(u.first_name, ' ', u.last_name) AS student,
                  r.status, r.reserved_at, r.notified_at, r.expires_at
             FROM reservations r
             JOIN users u ON u.user_id = r.user_id
            WHERE r.book_id = %s AND r.status IN ('PENDING', 'READY')
            ORDER BY r.reserved_at ASC""",
        (book_id,),
    )


def get_student_reservations(student_id):
    """A student's reservations, newest first."""
    user_id = _resolve_user_id(student_id)
    return execute_query(
        """SELECT r.reservation_id, b.title, r.status,
                  r.reserved_at, r.expires_at
             FROM reservations r
             JOIN books b ON b.book_id = r.book_id
            WHERE r.user_id = %s
            ORDER BY r.reserved_at DESC""",
        (user_id,),
    )


def hold_book(book_id: int) -> str:
    """Physically set aside an available copy by marking it RESERVED (for pickup)."""
    copies = execute_query(
        "SELECT copy_id FROM book_copies "
        "WHERE book_id = %s AND status = 'AVAILABLE' LIMIT 1",
        (book_id,),
    )
    if not copies:
        return f"No available copy of book {book_id} to hold."
    copy_id = copies[0][0]
    execute_transaction(
        [
            ("UPDATE book_copies SET status = 'RESERVED' WHERE copy_id = %s", (copy_id,)),
            (
                "UPDATE books SET available_copies = available_copies - 1 "
                "WHERE book_id = %s AND available_copies > 0",
                (book_id,),
            ),
        ]
    )
    return f"Held copy {copy_id} of book {book_id}."


def release_hold(copy_id: int) -> str:
    """Release a held copy back to AVAILABLE."""
    rows = execute_query(
        "SELECT book_id FROM book_copies WHERE copy_id = %s AND status = 'RESERVED'",
        (copy_id,),
    )
    if not rows:
        return f"Copy {copy_id} is not currently held."
    book_id = rows[0][0]
    execute_transaction(
        [
            ("UPDATE book_copies SET status = 'AVAILABLE' WHERE copy_id = %s", (copy_id,)),
            (
                "UPDATE books SET available_copies = available_copies + 1 "
                "WHERE book_id = %s",
                (book_id,),
            ),
        ]
    )
    return f"Released hold on copy {copy_id}."


# ===========================================================================
# Damage & lost-book handling
# ===========================================================================
def process_damage(
    student_id,
    book_id: int,
    description: str,
    damage_type: str = "OTHER",
    estimated_cost: float = 0.0,
    librarian=DEFAULT_LIBRARIAN,
    date: str | None = None,
) -> dict:
    """
    Record damage to a book the student last handled: file a damage report, mark
    the copy DAMAGED, and assess a DAMAGE fine for the estimated cost.
    """
    user_id = _resolve_user_id(student_id)
    lib_id = _resolve_librarian_id(librarian)
    when = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    loans = execute_query(
        """SELECT l.loan_id, l.copy_id
             FROM loan_transactions l
             JOIN book_copies c ON c.copy_id = l.copy_id
            WHERE l.borrower_user_id = %s AND c.book_id = %s
            ORDER BY l.issued_at DESC
            LIMIT 1""",
        (user_id, book_id),
    )
    if not loans:
        raise ValueError(
            f"No loan history for user {student_id} and book {book_id}"
        )
    loan_id, copy_id = loans[0]

    report_id = execute_transaction(
        [
            (
                """INSERT INTO damage_reports
                     (loan_id, copy_id, reported_by_user_id,
                      reported_by_librarian_id, reported_at, damage_type,
                      description, estimated_cost, resolution_status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'CHARGED')""",
                (
                    loan_id, copy_id, user_id, lib_id, when,
                    damage_type, description, estimated_cost,
                ),
            )
        ]
    )[0]

    steps = [
        (
            """INSERT INTO book_ledger_entries
                 (book_id, copy_id, damage_report_id, entry_type, entry_date,
                  quantity, notes)
               VALUES (%s, %s, %s, 'DAMAGE', %s, 1, %s)""",
            (book_id, copy_id, report_id, when, description),
        ),
        ("UPDATE book_copies SET status = 'DAMAGED' WHERE copy_id = %s", (copy_id,)),
    ]
    if estimated_cost and estimated_cost > 0:
        steps.append(
            (
                """INSERT INTO fines
                     (loan_id, damage_report_id, user_id, fine_type, assessed_at,
                      due_date, amount, status, remarks)
                   VALUES (%s, %s, %s, 'DAMAGE', %s,
                           DATE_ADD(%s, INTERVAL %s DAY), %s, 'UNPAID', %s)""",
                (
                    loan_id, report_id, user_id, when, when,
                    FINE_GRACE_DAYS, estimated_cost, description,
                ),
            )
        )
        steps.append(_upsert_fine_assessed(user_id, float(estimated_cost)))

    execute_transaction(steps)
    return {
        "damage_report_id": report_id,
        "copy_id": copy_id,
        "fine_assessed": float(estimated_cost or 0),
    }


def process_lost_book(
    student_id,
    book_id: int,
    replacement_cost: float,
    librarian=DEFAULT_LIBRARIAN,
    date: str | None = None,
) -> dict:
    """
    Mark a book lost: close the loan as LOST, mark the copy LOST, drop a LOSS
    ledger entry, and charge the replacement cost as a LOST_BOOK fine.
    """
    user_id = _resolve_user_id(student_id)
    lib_id = _resolve_librarian_id(librarian)
    when = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    loans = execute_query(
        """SELECT l.loan_id, l.copy_id
             FROM loan_transactions l
             JOIN book_copies c ON c.copy_id = l.copy_id
            WHERE l.borrower_user_id = %s AND c.book_id = %s
              AND l.status IN ('ISSUED', 'OVERDUE')
            ORDER BY l.issued_at ASC
            LIMIT 1""",
        (user_id, book_id),
    )
    if not loans:
        raise ValueError(
            f"No active loan found for user {student_id} and book {book_id}"
        )
    loan_id, copy_id = loans[0]

    steps = [
        (
            """UPDATE loan_transactions
                  SET status = 'LOST', returned_by_librarian_id = %s
                WHERE loan_id = %s""",
            (lib_id, loan_id),
        ),
        ("UPDATE book_copies SET status = 'LOST' WHERE copy_id = %s", (copy_id,)),
        (
            "UPDATE books SET total_copies = GREATEST(total_copies - 1, 0) "
            "WHERE book_id = %s",
            (book_id,),
        ),
        (
            """INSERT INTO book_ledger_entries
                 (book_id, copy_id, loan_id, entry_type, entry_date, quantity, notes)
               VALUES (%s, %s, %s, 'LOSS', %s, 1, 'Reported lost')""",
            (book_id, copy_id, loan_id, when),
        ),
        (
            """INSERT INTO fines
                 (loan_id, user_id, fine_type, assessed_at, due_date,
                  amount, status, remarks)
               VALUES (%s, %s, 'LOST_BOOK', %s,
                       DATE_ADD(%s, INTERVAL %s DAY), %s, 'UNPAID',
                       'Replacement cost for lost book')""",
            (loan_id, user_id, when, when, FINE_GRACE_DAYS, replacement_cost),
        ),
        _upsert_fine_assessed(user_id, float(replacement_cost)),
    ]
    execute_transaction(steps)
    return {
        "loan_id": loan_id,
        "copy_id": copy_id,
        "fine_assessed": float(replacement_cost),
    }


# ===========================================================================
# Student-facing helpers
# ===========================================================================
def deactivate_student(student_id, status: str = "INACTIVE") -> str:
    """Deactivate a student account (status INACTIVE / BLOCKED / LEFT)."""
    user_id = _resolve_user_id(student_id)
    execute_query(
        "UPDATE users SET status = %s WHERE user_id = %s", (status, user_id)
    )
    return f"User {student_id} set to {status}."


def get_student_loans(student_id, active_only: bool = True):
    """Books a student currently holds (or their full loan history)."""
    user_id = _resolve_user_id(student_id)
    clause = "AND l.status IN ('ISSUED', 'OVERDUE')" if active_only else ""
    return execute_query(
        f"""SELECT l.loan_id, b.book_id, b.title, c.barcode,
                   l.issued_at, l.due_at, l.returned_at, l.status
              FROM loan_transactions l
              JOIN book_copies c ON c.copy_id = l.copy_id
              JOIN books b       ON b.book_id = c.book_id
             WHERE l.borrower_user_id = %s {clause}
             ORDER BY l.issued_at DESC""",
        (user_id,),
    )


# ===========================================================================
# Analytics: performance & summaries (prompt-backing queries)
# ===========================================================================
def top_performing_books(limit: int = 10):
    """Most-issued books."""
    return execute_query(
        "SELECT * FROM v_book_issue_stats "
        "ORDER BY total_issues DESC, title ASC LIMIT %s",
        (limit,),
    )


def under_performing_books():
    """Books issued at least once but below the average issue count."""
    return execute_query(
        """SELECT s.*
             FROM v_book_issue_stats s
            WHERE s.total_issues > 0
              AND s.total_issues < (SELECT AVG(total_issues) FROM v_book_issue_stats)
            ORDER BY s.total_issues ASC, s.title ASC"""
    )


def low_performing_books(max_issues: int = 3):
    """Books with very few issues (0..max_issues) — candidates for retiring."""
    return execute_query(
        """SELECT s.*
             FROM v_book_issue_stats s
            WHERE s.total_issues BETWEEN 0 AND %s
            ORDER BY s.total_issues ASC, s.title ASC""",
        (max_issues,),
    )


def shortage_books(threshold: int = 1):
    """Active books at or below a low availability threshold (possible reorders)."""
    return execute_query(
        """SELECT book_id, title, subject, available_copies, total_copies
             FROM books
            WHERE active = TRUE AND available_copies <= %s
            ORDER BY available_copies ASC, title ASC""",
        (threshold,),
    )


def monthly_fine_collection():
    """Fine collection grouped by month (newest first)."""
    return execute_query(
        "SELECT * FROM v_monthly_fine_collection ORDER BY month_key DESC"
    )


def monthly_book_ledger():
    """Book ledger movement grouped by month and entry type."""
    return execute_query(
        "SELECT * FROM v_monthly_book_ledger "
        "ORDER BY month_key DESC, entry_type ASC"
    )


def quarterly_fine_summary(year: int, quarter: int) -> dict:
    """Fines collected during a calendar quarter."""
    start, end = _quarter_range(year, quarter)
    total = execute_query(
        """SELECT COUNT(*) AS payments, COALESCE(SUM(amount), 0) AS total_collected
             FROM fine_payments
            WHERE paid_at >= %s AND paid_at < %s""",
        (start, end),
    )
    by_month = execute_query(
        # %% escapes the literal % for the connector's parameter substitution.
        """SELECT DATE_FORMAT(paid_at, '%%Y-%%m') AS month_key,
                  COUNT(*) AS payments, SUM(amount) AS collected
             FROM fine_payments
            WHERE paid_at >= %s AND paid_at < %s
            GROUP BY DATE_FORMAT(paid_at, '%%Y-%%m')
            ORDER BY month_key""",
        (start, end),
    )
    return {
        "year": year,
        "quarter": quarter,
        "range": [start, end],
        "totals": total[0],
        "by_month": by_month,
    }


def quarterly_circulation_summary(year: int, quarter: int) -> dict:
    """Issue / return / other ledger activity during a calendar quarter."""
    start, end = _quarter_range(year, quarter)
    by_type = execute_query(
        """SELECT entry_type, COUNT(*) AS entries,
                  COALESCE(SUM(quantity), 0) AS quantity
             FROM book_ledger_entries
            WHERE entry_date >= %s AND entry_date < %s
            GROUP BY entry_type
            ORDER BY entry_type""",
        (start, end),
    )
    return {
        "year": year,
        "quarter": quarter,
        "range": [start, end],
        "by_type": by_type,
    }


# ===========================================================================
# Library policies (configurable rules)
# ===========================================================================
def update_policy(policy_id, new_policy: str, description: str | None = None) -> str:
    """
    Update a policy value. `policy_id` may be the numeric id or the policy_key
    (e.g. 'fine_per_day'). `new_policy` is the new value to store.
    """
    if isinstance(policy_id, int) or str(policy_id).isdigit():
        column, key = "policy_id", int(policy_id)
    else:
        column, key = "policy_key", policy_id
    execute_query(
        f"""UPDATE library_policies
               SET policy_value = %s,
                   description  = COALESCE(%s, description)
             WHERE {column} = %s""",
        (new_policy, description, key),
    )
    return f"Policy {policy_id!r} updated to {new_policy!r}."


def get_policy(policy_key: str):
    """Fetch a single policy by its key."""
    return execute_query(
        "SELECT policy_id, policy_key, policy_value, description, updated_at "
        "FROM library_policies WHERE policy_key = %s",
        (policy_key,),
    )


def get_policies():
    """List all configured library policies."""
    return execute_query(
        "SELECT policy_id, policy_key, policy_value, description, updated_at "
        "FROM library_policies ORDER BY policy_key"
    )


# ===========================================================================
# Journals & article subscriptions
# ===========================================================================
def add_journal(title: str, issn: str | None = None,
                publisher_id: int | None = None, subject: str | None = None,
                frequency: str = "MONTHLY") -> int:
    """Register a journal/periodical the library tracks. Returns journal_id."""
    return execute_transaction(
        [
            (
                """INSERT INTO journals (title, issn, publisher_id, subject, frequency)
                   VALUES (%s, %s, %s, %s, %s)""",
                (title, issn, publisher_id, subject, frequency),
            )
        ]
    )[0]


def add_subscription(journal_id: int, start_date: str, end_date: str,
                     cost: float = 0.0, access_type: str = "BOTH",
                     vendor: str | None = None) -> int:
    """Create an article/journal subscription contract. Returns subscription_id."""
    return execute_transaction(
        [
            (
                """INSERT INTO journal_subscriptions
                     (journal_id, start_date, end_date, cost, access_type,
                      vendor, status)
                   VALUES (%s, %s, %s, %s, %s, %s, 'ACTIVE')""",
                (journal_id, start_date, end_date, cost, access_type, vendor),
            )
        ]
    )[0]


def cancel_subscription(subscription_id: int) -> str:
    """Cancel a journal subscription."""
    execute_query(
        "UPDATE journal_subscriptions SET status = 'CANCELLED' "
        "WHERE subscription_id = %s",
        (subscription_id,),
    )
    return f"Subscription {subscription_id} cancelled."


def renew_subscription(subscription_id: int, new_end_date: str,
                       cost: float | None = None) -> str:
    """Extend a subscription to a new end date and reactivate it."""
    execute_query(
        """UPDATE journal_subscriptions
              SET end_date = %s,
                  cost     = COALESCE(%s, cost),
                  status   = 'ACTIVE'
            WHERE subscription_id = %s""",
        (new_end_date, cost, subscription_id),
    )
    return f"Subscription {subscription_id} renewed to {new_end_date}."


def get_active_subscriptions():
    """All currently active subscriptions with journal details."""
    return execute_query(
        """SELECT s.subscription_id, j.title, j.issn, j.subject,
                  s.start_date, s.end_date, s.cost, s.access_type,
                  s.vendor, s.status
             FROM journal_subscriptions s
             JOIN journals j ON j.journal_id = s.journal_id
            WHERE s.status = 'ACTIVE'
            ORDER BY s.end_date ASC"""
    )


def get_journal_catalog():
    """List all journals the library tracks."""
    return execute_query(
        """SELECT j.journal_id, j.title, j.issn, j.subject, j.frequency,
                  p.publisher_name
             FROM journals j
             LEFT JOIN publishers p ON p.publisher_id = j.publisher_id
            ORDER BY j.title"""
    )


# ===========================================================================
# Notifications
# ===========================================================================
def notify(student_id, message: str, channel: str = "SYSTEM",
           subject: str | None = None, reason: str | None = None,
           related_table: str | None = None,
           related_id: int | None = None) -> int:
    """Log an outbound notification to a student. Returns notification_id."""
    user_id = _resolve_user_id(student_id)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return execute_transaction(
        [
            (
                """INSERT INTO notifications
                     (user_id, channel, subject, message, reason,
                      related_table, related_id, status, sent_at)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, 'SENT', %s)""",
                (user_id, channel, subject, message, reason,
                 related_table, related_id, now),
            )
        ]
    )[0]


def notify_student_about_reservation(student_id, book_id: int,
                                     reason: str = "Your reserved book is ready") -> dict:
    """
    Tell a student their reserved book is ready: flip their PENDING reservation
    to READY and record the notification. Returns ids of both.
    """
    user_id = _resolve_user_id(student_id)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    reservations = execute_query(
        """SELECT reservation_id FROM reservations
            WHERE user_id = %s AND book_id = %s AND status = 'PENDING'
            ORDER BY reserved_at ASC LIMIT 1""",
        (user_id, book_id),
    )
    reservation_id = reservations[0][0] if reservations else None

    title_rows = execute_query("SELECT title FROM books WHERE book_id = %s", (book_id,))
    title = title_rows[0][0] if title_rows else f"book {book_id}"
    message = f'{reason}: "{title}" is ready for pickup.'

    steps = []
    if reservation_id is not None:
        steps.append(
            (
                """UPDATE reservations
                      SET status = 'READY', notified_at = %s
                    WHERE reservation_id = %s""",
                (now, reservation_id),
            )
        )
    steps.append(
        (
            """INSERT INTO notifications
                 (user_id, channel, subject, message, reason,
                  related_table, related_id, status, sent_at)
               VALUES (%s, 'EMAIL', 'Reserved book ready', %s,
                       'RESERVATION_READY', 'reservations', %s, 'SENT', %s)""",
            (user_id, message, reservation_id, now),
        )
    )
    results = execute_transaction(steps)
    notification_id = results[-1]
    return {"reservation_id": reservation_id, "notification_id": notification_id}


def get_notifications(student_id, limit: int = 20):
    """Recent notifications sent to a student."""
    user_id = _resolve_user_id(student_id)
    return execute_query(
        """SELECT notification_id, channel, subject, message, reason,
                  status, created_at
             FROM notifications
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT %s""",
        (user_id, limit),
    )


def send_return_reminders(date: str | None = None) -> list[int]:
    """
    Notify every borrower whose book is due today (used to 'track returns and
    send reminders'). Returns the notification ids created.
    """
    due = get_returns_due_today(date)
    ids: list[int] = []
    for loan_id, user_code, _email, _borrower, title, _barcode, due_at in due:
        ids.append(
            notify(
                user_code,
                message=f'Reminder: "{title}" is due on {due_at}. Please return on time.',
                channel="EMAIL",
                subject="Return reminder",
                reason="DUE_REMINDER",
                related_table="loan_transactions",
                related_id=loan_id,
            )
        )
    return ids


if __name__ == "__main__":
    # Read-only smoke checks (safe to run against the seeded database).
    print("Catalog:")
    for row in get_book_catalog():
        print(" ", row)

    print("\nPending returns:")
    for row in get_pending_returns():
        print(" ", row)

    print("\nOutstanding fines:")
    for row in get_outstanding_fines():
        print(" ", row)

    print("\nFine due for STU001:", get_fine_due("STU001"))
    print("Account balance STU001:", total_account_balance("STU001"))
    print("No-dues STU001:", issue_no_due_certificate("STU001"))

    print("\nTop performing books:")
    for row in top_performing_books(5):
        print(" ", row)

    print("\nQ1 2026 fine summary:", quarterly_fine_summary(2026, 1))
    print("Q1 2026 circulation:", quarterly_circulation_summary(2026, 1))
