from db import execute_query


def issue_book(student_id: str, book_id: int, date: str) -> str:
    query = "SELECT copy_id FROM book_copies WHERE book_id = %s AND status = %s LIMIT 1;"
    params = (book_id, 'AVAILABLE')
    book_copies = execute_query(query, params)
    print(book_copies)
    copy_id = book_copies[0][0]

    query = """INSERT INTO loan_transactions (
    copy_id,
    borrower_user_id,
    issued_by_librarian_id,
    issued_at,
    due_at,
    status
)
VALUES (
    %s,                 -- copy_id from above query
    %s,                 -- student_id
    %s,                 -- librarian_id
    %s,             -- issue date
    %s,
    %s
);
"""

    params = (copy_id, student_id, "LIBR001", date, date, "ACTIVE")


if __name__ == "__main__":
    issue_book("STU001", 1, "2023-05-15")
