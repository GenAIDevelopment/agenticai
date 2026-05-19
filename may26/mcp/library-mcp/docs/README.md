# College Library Database Design

## What this model covers

- **Books** as master data
- **Physical copies** so each issued book can be tracked individually
- **Users** with separate profiles for **Students** and **Librarians**
- **Transactions** for issuing, returning, damage reports, and fines
- **Accounts** for user balances and a consolidated library ledger
- **Analytics** for book performance and monthly financial/book movement summaries

## Main design choices

### 1. Normalize people and roles
`users` stores common identity fields, while `students` and `librarians` store role-specific details.

### 2. Track physical copies
A single title can have many copies. The `book_copies` table lets you track each barcode/accession number separately.

### 3. Separate loan, damage, and fine data
- `loan_transactions` tracks issue/return lifecycle
- `damage_reports` tracks incidents and resolution
- `fines` tracks charges
- `fine_payments` tracks payments

### 4. Keep reporting simple
`book_ledger_entries`, `v_book_issue_stats`, `v_monthly_fine_collection`, and `v_monthly_book_ledger` are designed so analytics can be queried without scanning raw business rules every time.

## Suggested workflow

1. Insert user records.
2. Insert role records in `students` or `librarians`.
3. Add books, authors, publishers, and copies.
4. Record issue/return activity in `loan_transactions`.
5. Create damage reports and fines when needed.
6. Record payments and ledger entries.
7. Run analytics from the provided views/queries.

## Notes

- `available_copies` in `books` is a cache field. You can update it from the application layer or by triggers.
- The analytics thresholds for under/low performing books are adjustable.
- If you want, the next step can be a version with **triggers and stored procedures** to auto-update copy status and balances.
