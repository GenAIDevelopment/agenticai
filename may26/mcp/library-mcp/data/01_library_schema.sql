-- library_schema.sql
-- MySQL 8+ schema for a college library management system

CREATE DATABASE IF NOT EXISTS library
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE library;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS library_account_ledger;
DROP TABLE IF EXISTS user_accounts;
DROP TABLE IF EXISTS book_ledger_entries;
DROP TABLE IF EXISTS fine_payments;
DROP TABLE IF EXISTS fines;
DROP TABLE IF EXISTS damage_reports;
DROP TABLE IF EXISTS loan_transactions;
DROP TABLE IF EXISTS book_copies;
DROP TABLE IF EXISTS book_authors;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS publishers;
DROP TABLE IF EXISTS librarians;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS users;

SET FOREIGN_KEY_CHECKS = 1;

-- ------------------------------------------------------------
-- 1) USERS & ROLES
-- ------------------------------------------------------------
CREATE TABLE users (
    user_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_code VARCHAR(20) NOT NULL,
    user_type ENUM('STUDENT', 'LIBRARIAN') NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NULL,
    password_hash VARCHAR(255) NOT NULL,
    status ENUM('ACTIVE', 'INACTIVE', 'BLOCKED', 'LEFT') NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id),
    UNIQUE KEY uk_users_user_code (user_code),
    UNIQUE KEY uk_users_email (email),
    KEY idx_users_type_status (user_type, status)
) ENGINE=InnoDB;

CREATE TABLE students (
    student_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    roll_no VARCHAR(30) NOT NULL,
    admission_no VARCHAR(30) NULL,
    department VARCHAR(100) NOT NULL,
    program VARCHAR(100) NULL,
    year_of_study TINYINT UNSIGNED NULL,
    admission_year YEAR NULL,
    valid_upto DATE NULL,
    PRIMARY KEY (student_id),
    UNIQUE KEY uk_students_user_id (user_id),
    UNIQUE KEY uk_students_roll_no (roll_no),
    UNIQUE KEY uk_students_admission_no (admission_no),
    CONSTRAINT fk_students_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE librarians (
    librarian_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    employee_no VARCHAR(30) NOT NULL,
    designation VARCHAR(100) NULL,
    hire_date DATE NULL,
    active_from DATE NULL,
    active_to DATE NULL,
    PRIMARY KEY (librarian_id),
    UNIQUE KEY uk_librarians_user_id (user_id),
    UNIQUE KEY uk_librarians_employee_no (employee_no),
    CONSTRAINT fk_librarians_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 2) BOOK MASTER DATA
-- ------------------------------------------------------------
CREATE TABLE publishers (
    publisher_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    publisher_name VARCHAR(200) NOT NULL,
    website VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (publisher_id),
    UNIQUE KEY uk_publishers_name (publisher_name)
) ENGINE=InnoDB;

CREATE TABLE authors (
    author_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    author_name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (author_id),
    UNIQUE KEY uk_authors_name (author_name)
) ENGINE=InnoDB;

CREATE TABLE books (
    book_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    isbn13 VARCHAR(13) NULL,
    isbn10 VARCHAR(10) NULL,
    title VARCHAR(255) NOT NULL,
    subtitle VARCHAR(255) NULL,
    edition VARCHAR(50) NULL,
    publisher_id BIGINT UNSIGNED NULL,
    publication_year YEAR NULL,
    language VARCHAR(50) NULL,
    subject VARCHAR(120) NULL,
    description TEXT NULL,
    pages INT UNSIGNED NULL,
    call_number VARCHAR(50) NULL,
    shelf_location VARCHAR(50) NULL,
    total_copies INT UNSIGNED NOT NULL DEFAULT 0,
    available_copies INT UNSIGNED NOT NULL DEFAULT 0,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (book_id),
    UNIQUE KEY uk_books_isbn13 (isbn13),
    UNIQUE KEY uk_books_isbn10 (isbn10),
    KEY idx_books_title (title),
    KEY idx_books_subject (subject),
    KEY idx_books_publisher (publisher_id),
    CONSTRAINT fk_books_publisher
        FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE book_authors (
    book_id BIGINT UNSIGNED NOT NULL,
    author_id BIGINT UNSIGNED NOT NULL,
    is_primary_author BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (book_id, author_id),
    CONSTRAINT fk_book_authors_book
        FOREIGN KEY (book_id) REFERENCES books(book_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_book_authors_author
        FOREIGN KEY (author_id) REFERENCES authors(author_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE book_copies (
    copy_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    book_id BIGINT UNSIGNED NOT NULL,
    barcode VARCHAR(50) NOT NULL,
    accession_no VARCHAR(50) NOT NULL,
    status ENUM('AVAILABLE', 'ISSUED', 'RESERVED', 'DAMAGED', 'LOST', 'WITHDRAWN') NOT NULL DEFAULT 'AVAILABLE',
    condition_status ENUM('NEW', 'GOOD', 'FAIR', 'POOR', 'DAMAGED') NOT NULL DEFAULT 'GOOD',
    acquired_date DATE NULL,
    purchase_price DECIMAL(10,2) NULL,
    notes VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (copy_id),
    UNIQUE KEY uk_book_copies_barcode (barcode),
    UNIQUE KEY uk_book_copies_accession_no (accession_no),
    KEY idx_book_copies_book_status (book_id, status),
    CONSTRAINT fk_book_copies_book
        FOREIGN KEY (book_id) REFERENCES books(book_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 3) CIRCULATION & TRANSACTIONS
-- ------------------------------------------------------------
CREATE TABLE loan_transactions (
    loan_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    copy_id BIGINT UNSIGNED NOT NULL,
    borrower_user_id BIGINT UNSIGNED NOT NULL,
    issued_by_librarian_id BIGINT UNSIGNED NOT NULL,
    issued_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_at DATETIME NOT NULL,
    returned_at DATETIME NULL,
    returned_by_librarian_id BIGINT UNSIGNED NULL,
    issue_condition ENUM('NEW', 'GOOD', 'FAIR', 'POOR', 'DAMAGED') NOT NULL DEFAULT 'GOOD',
    return_condition ENUM('NEW', 'GOOD', 'FAIR', 'POOR', 'DAMAGED') NULL,
    renewal_count SMALLINT UNSIGNED NOT NULL DEFAULT 0,
    status ENUM('ISSUED', 'RETURNED', 'OVERDUE', 'LOST', 'DAMAGED', 'CANCELLED') NOT NULL DEFAULT 'ISSUED',
    notes TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (loan_id),
    KEY idx_loans_copy_status (copy_id, status),
    KEY idx_loans_borrower_status (borrower_user_id, status),
    KEY idx_loans_due_at (due_at),
    KEY idx_loans_issued_at (issued_at),
    CONSTRAINT fk_loans_copy
        FOREIGN KEY (copy_id) REFERENCES book_copies(copy_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_loans_borrower_user
        FOREIGN KEY (borrower_user_id) REFERENCES users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_loans_issued_by_librarian
        FOREIGN KEY (issued_by_librarian_id) REFERENCES librarians(librarian_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_loans_returned_by_librarian
        FOREIGN KEY (returned_by_librarian_id) REFERENCES librarians(librarian_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE damage_reports (
    damage_report_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    loan_id BIGINT UNSIGNED NULL,
    copy_id BIGINT UNSIGNED NOT NULL,
    reported_by_user_id BIGINT UNSIGNED NOT NULL,
    reported_by_librarian_id BIGINT UNSIGNED NOT NULL,
    reported_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    damage_type ENUM('MINOR', 'MAJOR', 'LOST', 'MISSING_PAGES', 'WATER_DAMAGE', 'TEAR', 'OTHER') NOT NULL DEFAULT 'OTHER',
    description TEXT NOT NULL,
    estimated_cost DECIMAL(10,2) NULL,
    resolution_status ENUM('OPEN', 'CHARGED', 'WAIVED', 'PAID', 'REPAIRED', 'REPLACED') NOT NULL DEFAULT 'OPEN',
    resolved_at DATETIME NULL,
    PRIMARY KEY (damage_report_id),
    KEY idx_damage_copy (copy_id),
    KEY idx_damage_loan (loan_id),
    KEY idx_damage_reported_at (reported_at),
    CONSTRAINT fk_damage_loan
        FOREIGN KEY (loan_id) REFERENCES loan_transactions(loan_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_damage_copy
        FOREIGN KEY (copy_id) REFERENCES book_copies(copy_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_damage_reported_by_user
        FOREIGN KEY (reported_by_user_id) REFERENCES users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_damage_reported_by_librarian
        FOREIGN KEY (reported_by_librarian_id) REFERENCES librarians(librarian_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE fines (
    fine_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    loan_id BIGINT UNSIGNED NULL,
    damage_report_id BIGINT UNSIGNED NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    fine_type ENUM('LATE_RETURN', 'DAMAGE', 'LOST_BOOK', 'OTHER') NOT NULL DEFAULT 'OTHER',
    assessed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_date DATE NULL,
    amount DECIMAL(10,2) NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    status ENUM('UNPAID', 'PARTIALLY_PAID', 'PAID', 'WAIVED', 'CANCELLED') NOT NULL DEFAULT 'UNPAID',
    remarks TEXT NULL,
    PRIMARY KEY (fine_id),
    KEY idx_fines_user_status (user_id, status),
    KEY idx_fines_assessed_at (assessed_at),
    KEY idx_fines_loan (loan_id),
    KEY idx_fines_damage (damage_report_id),
    CONSTRAINT fk_fines_loan
        FOREIGN KEY (loan_id) REFERENCES loan_transactions(loan_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_fines_damage
        FOREIGN KEY (damage_report_id) REFERENCES damage_reports(damage_report_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_fines_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE fine_payments (
    payment_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    fine_id BIGINT UNSIGNED NOT NULL,
    paid_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('CASH', 'CARD', 'UPI', 'BANK_TRANSFER', 'WAIVER') NOT NULL DEFAULT 'CASH',
    received_by_librarian_id BIGINT UNSIGNED NULL,
    receipt_no VARCHAR(50) NULL,
    notes VARCHAR(255) NULL,
    PRIMARY KEY (payment_id),
    UNIQUE KEY uk_fine_payments_receipt_no (receipt_no),
    KEY idx_fine_payments_fine (fine_id),
    KEY idx_fine_payments_paid_at (paid_at),
    CONSTRAINT fk_fine_payments_fine
        FOREIGN KEY (fine_id) REFERENCES fines(fine_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_fine_payments_received_by_librarian
        FOREIGN KEY (received_by_librarian_id) REFERENCES librarians(librarian_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Ledger logging for all physical circulation items
CREATE TABLE book_ledger_entries (
    book_ledger_entry_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    book_id BIGINT UNSIGNED NOT NULL,
    copy_id BIGINT UNSIGNED NULL,
    loan_id BIGINT UNSIGNED NULL,
    damage_report_id BIGINT UNSIGNED NULL,
    entry_type ENUM('ACQUISITION', 'ISSUE', 'RETURN', 'RENEWAL', 'DAMAGE', 'LOSS', 'WITHDRAWAL', 'ADJUSTMENT') NOT NULL,
    entry_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    quantity INT NOT NULL DEFAULT 1,
    notes VARCHAR(255) NULL,
    PRIMARY KEY (book_ledger_entry_id),
    KEY idx_book_ledger_book_date (book_id, entry_date),
    KEY idx_book_ledger_entry_type_date (entry_type, entry_date),
    CONSTRAINT fk_book_ledger_book
        FOREIGN KEY (book_id) REFERENCES books(book_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_book_ledger_copy
        FOREIGN KEY (copy_id) REFERENCES book_copies(copy_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_book_ledger_loan
        FOREIGN KEY (loan_id) REFERENCES loan_transactions(loan_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_book_ledger_damage
        FOREIGN KEY (damage_report_id) REFERENCES damage_reports(damage_report_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 4) FINANCIAL BALANCES & LEDGERS
-- ------------------------------------------------------------
CREATE TABLE user_accounts (
    user_id BIGINT UNSIGNED NOT NULL,
    opening_balance DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total_fines_assessed DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total_payments_received DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total_waived DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    current_balance DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id),
    CONSTRAINT fk_user_accounts_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE library_account_ledger (
    library_account_ledger_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    entry_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    entry_type ENUM('FINE_COLLECTED', 'WAIVED', 'REPAIR_COST', 'BOOK_PURCHASE', 'REFUND', 'OTHER') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    reference_table VARCHAR(50) NULL,
    reference_id BIGINT UNSIGNED NULL,
    description VARCHAR(255) NULL,
    PRIMARY KEY (library_account_ledger_id),
    KEY idx_library_ledger_date (entry_date),
    KEY idx_library_ledger_type_date (entry_type, entry_date)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- 5) ANALYTICS VIEWS
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW v_book_issue_stats AS
SELECT
    b.book_id,
    b.isbn13,
    b.title,
    b.subject,
    COUNT(l.loan_id) AS total_issues,
    SUM(CASE WHEN l.status = 'RETURNED' THEN 1 ELSE 0 END) AS total_returns,
    SUM(CASE WHEN l.status = 'OVERDUE' THEN 1 ELSE 0 END) AS overdue_loans,
    SUM(CASE WHEN l.status IN ('DAMAGED', 'LOST') THEN 1 ELSE 0 END) AS problem_loans
FROM books b
LEFT JOIN book_copies c ON c.book_id = b.book_id
LEFT JOIN loan_transactions l ON l.copy_id = c.copy_id
GROUP BY b.book_id, b.isbn13, b.title, b.subject;

CREATE OR REPLACE VIEW v_monthly_fine_collection AS
SELECT
    DATE_FORMAT(fp.paid_at, '%Y-%m') AS month_key,
    COUNT(*) AS payment_count,
    SUM(fp.amount) AS total_collected
FROM fine_payments fp
GROUP BY DATE_FORMAT(fp.paid_at, '%Y-%m');

CREATE OR REPLACE VIEW v_monthly_book_ledger AS
SELECT
    DATE_FORMAT(ble.entry_date, '%Y-%m') AS month_key,
    ble.entry_type,
    COUNT(*) AS entry_count,
    SUM(ble.quantity) AS total_quantity
FROM book_ledger_entries ble
GROUP BY DATE_FORMAT(ble.entry_date, '%Y-%m'), ble.entry_type;