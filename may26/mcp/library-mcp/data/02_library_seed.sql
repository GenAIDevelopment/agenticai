-- library_seed.sql
-- Fills the college library schema with robust multi-month transactional data

USE library;

-- ------------------------------------------------------------
-- 1) USER ACCOUNTS SEEDING
-- ------------------------------------------------------------
INSERT INTO users (user_id, user_code, user_type, first_name, last_name, email, phone, password_hash, status) VALUES
(1, 'EMP001', 'LIBRARIAN', 'Sarah', 'Connor', 'sarah.c@library.edu', '555-0101', 'securehash123', 'ACTIVE'),
(2, 'EMP002', 'LIBRARIAN', 'James', 'Smith', 'james.s@library.edu', '555-0102', 'securehash456', 'ACTIVE'),
(3, 'STU001', 'STUDENT', 'John', 'Doe', 'john.doe@student.edu', '555-0201', 'studenthash1', 'ACTIVE'),
(4, 'STU002', 'STUDENT', 'Jane', 'Watson', 'jane.w@student.edu', '555-0202', 'studenthash2', 'ACTIVE'),
(5, 'STU003', 'STUDENT', 'Alex', 'Mercer', 'alex.m@student.edu', '555-0203', 'studenthash3', 'ACTIVE');

INSERT INTO librarians (librarian_id, user_id, employee_no, designation, hire_date, active_from) VALUES
(1, 1, 'EMP001', 'Head Librarian', '2020-01-15', '2020-01-15'),
(2, 2, 'EMP002', 'Assistant Assistant', '2022-06-01', '2022-06-01');

INSERT INTO students (student_id, user_id, roll_no, admission_no, department, program, year_of_study, admission_year, valid_upto) VALUES
(1, 3, 'CS2023-089', 'ADM-9901', 'Computer Science', 'B.Tech', 3, 2023, '2027-06-30'),
(2, 4, 'EE2024-012', 'ADM-9942', 'Electrical Engineering', 'M.Tech', 2, 2024, '2026-06-30'),
(3, 5, 'ME2025-003', 'ADM-1010', 'Mechanical Engineering', 'B.Tech', 1, 2025, '2029-06-30');

-- ------------------------------------------------------------
-- 2) BOOK META DATA & COPIES SEEDING
-- ------------------------------------------------------------
INSERT INTO publishers (publisher_id, publisher_name, website) VALUES
(1, 'O Reilly Media', 'https://oreilly.com'),
(2, 'MIT Press', 'https://mitpress.mit.edu'),
(3, 'Oxford University Press', 'https://oup.com');

INSERT INTO authors (author_id, author_name) VALUES
(1, 'Thomas H. Cormen'),
(2, 'Robert C. Martin'),
(3, 'Charles E. Leiserson'),
(4, 'Gilbert Strang');

-- Books Catalog Profiles
-- Book 1 & 2: Designed to be High Performers
-- Book 3 & 4: Designed to be Under Performers
-- Book 5 & 6: Designed to be Low/No Performers
INSERT INTO books (book_id, isbn13, title, publisher_id, publication_year, subject, total_copies, available_copies) VALUES
(1, '9780262033848', 'Introduction to Algorithms', 2, 2009, 'Computer Science', 3, 1),
(2, '9780132350884', 'Clean Code', 1, 2008, 'Computer Science', 2, 0),
(3, '9780961408817', 'Introduction to Linear Algebra', 3, 2016, 'Mathematics', 2, 2),
(4, '9780262510875', 'Structure and Interpretation of Computer Programs', 2, 1996, 'Computer Science', 1, 1),
(5, '9780198520115', 'Oxford Classical History Atlas', 3, 2002, 'History', 1, 1),
(6, '9781449331818', 'Learning Python', 1, 2013, 'Computer Science', 2, 2);

INSERT INTO book_authors (book_id, author_id, is_primary_author) VALUES
(1, 1, TRUE),
(1, 3, FALSE),
(2, 2, TRUE),
(3, 4, TRUE);

-- Physical copy components
INSERT INTO book_copies (copy_id, book_id, barcode, accession_no, status, condition_status, purchase_price) VALUES
(1, 1, 'BC-ALGO-001', 'ACC-1001', 'ISSUED', 'GOOD', 120.00),
(2, 1, 'BC-ALGO-002', 'ACC-1002', 'AVAILABLE', 'GOOD', 120.00),
(3, 1, 'BC-ALGO-003', 'ACC-1003', 'AVAILABLE', 'NEW', 125.00),
(4, 2, 'BC-CODE-001', 'ACC-2001', 'ISSUED', 'FAIR', 85.00),
(5, 2, 'BC-CODE-002', 'ACC-2002', 'ISSUED', 'GOOD', 85.00),
(6, 3, 'BC-LA-001', 'ACC-3001', 'AVAILABLE', 'NEW', 95.00),
(7, 3, 'BC-LA-002', 'ACC-3002', 'AVAILABLE', 'GOOD', 95.00),
(8, 4, 'BC-SICP-001', 'ACC-4001', 'AVAILABLE', 'POOR', 110.00),
(9, 5, 'BC-HIST-001', 'ACC-5001', 'AVAILABLE', 'GOOD', 60.00),
(10, 6, 'BC-PY-001', 'ACC-6001', 'AVAILABLE', 'NEW', 70.00),
(11, 6, 'BC-PY-002', 'ACC-6002', 'AVAILABLE', 'GOOD', 70.00);

-- Initial Asset Inventory Balance Logs
INSERT INTO book_ledger_entries (book_id, copy_id, entry_type, entry_date, quantity, notes) VALUES
(1, 1, 'ACQUISITION', '2026-01-05 10:00:00', 1, 'Initial inventory setup'),
(1, 2, 'ACQUISITION', '2026-01-05 10:00:00', 1, 'Initial inventory setup'),
(1, 3, 'ACQUISITION', '2026-01-05 10:00:00', 1, 'Initial inventory setup'),
(2, 4, 'ACQUISITION', '2026-01-05 10:30:00', 1, 'Initial inventory setup'),
(2, 5, 'ACQUISITION', '2026-01-05 10:30:00', 1, 'Initial inventory setup'),
(3, 6, 'ACQUISITION', '2026-01-06 09:00:00', 1, 'Initial inventory setup'),
(3, 7, 'ACQUISITION', '2026-01-06 09:00:00', 1, 'Initial inventory setup'),
(4, 8, 'ACQUISITION', '2026-01-06 09:15:00', 1, 'Initial inventory setup'),
(5, 9, 'ACQUISITION', '2026-01-07 14:00:00', 1, 'Initial inventory setup'),
(6, 10, 'ACQUISITION', '2026-01-10 11:00:00', 1, 'Initial inventory setup'),
(6, 11, 'ACQUISITION', '2026-01-10 11:00:00', 1, 'Initial inventory setup');

-- ------------------------------------------------------------
-- 3) MONTHLY CIRCULATION TRANSACTIONS (JANUARY - MAY 2026)
-- ------------------------------------------------------------

-- --- JANUARY 2026 ---
INSERT INTO loan_transactions (loan_id, copy_id, borrower_user_id, issued_by_librarian_id, issued_at, due_at, returned_at, returned_by_librarian_id, issue_condition, return_condition, status) VALUES
(1, 1, 3, 1, '2026-01-15 09:00:00', '2026-01-29 17:00:00', '2026-01-28 14:00:00', 1, 'GOOD', 'GOOD', 'RETURNED'),
(2, 4, 4, 1, '2026-01-16 10:30:00', '2026-01-30 17:00:00', '2026-01-30 16:00:00', 1, 'GOOD', 'FAIR', 'RETURNED');

INSERT INTO book_ledger_entries (book_id, copy_id, loan_id, entry_type, entry_date, quantity) VALUES
(1, 1, 1, 'ISSUE', '2026-01-15 09:00:00', 1),
(1, 1, 1, 'RETURN', '2026-01-28 14:00:00', 1),
(2, 4, 2, 'ISSUE', '2026-01-16 10:30:00', 1),
(2, 4, 2, 'RETURN', '2026-01-30 16:00:00', 1);

-- --- FEBRUARY 2026 (Generates late fines) ---
INSERT INTO loan_transactions (loan_id, copy_id, borrower_user_id, issued_by_librarian_id, issued_at, due_at, returned_at, returned_by_librarian_id, issue_condition, return_condition, status) VALUES
(3, 1, 4, 1, '2026-02-01 11:00:00', '2026-02-15 17:00:00', '2026-02-20 12:00:00', 2, 'GOOD', 'GOOD', 'RETURNED'),
(4, 5, 5, 2, '2026-02-05 14:00:00', '2026-02-19 17:00:00', '2026-02-18 09:30:00', 1, 'GOOD', 'GOOD', 'RETURNED');

INSERT INTO book_ledger_entries (book_id, copy_id, loan_id, entry_type, entry_date, quantity) VALUES
(1, 1, 3, 'ISSUE', '2026-02-01 11:00:00', 1),
(1, 1, 3, 'RETURN', '2026-02-20 12:00:00', 1),
(2, 5, 4, 'ISSUE', '2026-02-05 14:00:00', 1),
(2, 5, 4, 'RETURN', '2026-02-18 09:30:00', 1);

-- Late Fine Assessment for Feb transaction (Returned 5 days late @ $10.00/day = $50.00)
INSERT INTO fines (fine_id, loan_id, user_id, fine_type, assessed_at, due_date, amount, amount_paid, status, remarks) VALUES
(1, 3, 4, 'LATE_RETURN', '2026-02-20 12:05:00', '2026-03-10', 50.00, 50.00, 'PAID', '5 Days overdue');

INSERT INTO fine_payments (payment_id, fine_id, paid_at, amount, payment_method, received_by_librarian_id, receipt_no) VALUES
(1, 1, '2026-02-22 10:00:00', 50.00, 'UPI', 2, 'REC-2026-001');

INSERT INTO library_account_ledger (entry_date, entry_type, amount, reference_table, reference_id, description) VALUES
('2026-02-22 10:00:00', 'FINE_COLLECTED', 50.00, 'fine_payments', 1, 'Late return settlement from User ID 4');

-- --- MARCH 2026 (Generates a damage report + fine) ---
INSERT INTO loan_transactions (loan_id, copy_id, borrower_user_id, issued_by_librarian_id, issued_at, due_at, returned_at, returned_by_librarian_id, issue_condition, return_condition, status) VALUES
(5, 4, 3, 2, '2026-03-01 10:00:00', '2026-03-15 17:00:00', '2026-03-12 11:00:00', 1, 'FAIR', 'DAMAGED', 'RETURNED'),
(6, 6, 5, 1, '2026-03-10 15:00:00', '2026-03-24 17:00:00', '2026-03-24 10:00:00', 1, 'NEW', 'GOOD', 'RETURNED');

INSERT INTO book_ledger_entries (book_id, copy_id, loan_id, entry_type, entry_date, quantity) VALUES
(2, 4, 5, 'ISSUE', '2026-03-01 10:00:00', 1),
(2, 4, 5, 'RETURN', '2026-03-12 11:00:00', 1),
(3, 6, 6, 'ISSUE', '2026-03-10 15:00:00', 1),
(3, 6, 6, 'RETURN', '2026-03-24 10:00:00', 1);

INSERT INTO damage_reports (damage_report_id, loan_id, copy_id, reported_by_user_id, reported_by_librarian_id, reported_at, damage_type, description, estimated_cost, resolution_status, resolved_at) VALUES
(1, 5, 4, 3, 1, '2026-03-12 11:15:00', 'WATER_DAMAGE', 'Liquid stains across back index pages', 35.00, 'CHARGED', '2026-03-15 09:00:00');

INSERT INTO book_ledger_entries (book_id, copy_id, damage_report_id, entry_type, entry_date, quantity) VALUES
(2, 4, 1, 'DAMAGE', '2026-03-12 11:15:00', 1);

INSERT INTO fines (fine_id, loan_id, damage_report_id, user_id, fine_type, assessed_at, due_date, amount, amount_paid, status, remarks) VALUES
(2, 5, 1, 3, 'DAMAGE', '2026-03-15 09:00:00', '2026-04-15', 35.00, 35.00, 'PAID', 'Water damage compensation penalty');

INSERT INTO fine_payments (payment_id, fine_id, paid_at, amount, payment_method, received_by_librarian_id, receipt_no) VALUES
(2, 2, '2026-03-20 14:30:00', 35.00, 'CASH', 1, 'REC-2026-002');

INSERT INTO library_account_ledger (entry_date, entry_type, amount, reference_table, reference_id, description) VALUES
('2026-03-20 14:30:00', 'FINE_COLLECTED', 35.00, 'fine_payments', 2, 'Liquid damage fee user 3');

-- --- APRIL 2026 (Generates fine collected + a partial payment entry) ---
INSERT INTO loan_transactions (loan_id, copy_id, borrower_user_id, issued_by_librarian_id, issued_at, due_at, returned_at, returned_by_librarian_id, issue_condition, return_condition, status) VALUES
(7, 1, 5, 1, '2026-04-01 09:30:00', '2026-04-15 17:00:00', '2026-04-25 12:00:00', 2, 'GOOD', 'GOOD', 'RETURNED'),
(8, 2, 3, 2, '2026-04-10 11:00:00', '2026-04-24 17:00:00', '2026-04-24 09:00:00', 2, 'GOOD', 'GOOD', 'RETURNED'),
(9, 7, 4, 1, '2026-04-12 14:00:00', '2026-04-26 17:00:00', '2026-04-25 15:00:00', 1, 'GOOD', 'GOOD', 'RETURNED');

INSERT INTO book_ledger_entries (book_id, copy_id, loan_id, entry_type, entry_date, quantity) VALUES
(1, 1, 7, 'ISSUE', '2026-04-01 09:30:00', 1),
(1, 1, 7, 'RETURN', '2026-04-25 12:00:00', 1),
(1, 2, 8, 'ISSUE', '2026-04-10 11:00:00', 1),
(1, 2, 8, 'RETURN', '2026-04-24 09:00:00', 1),
(3, 7, 9, 'ISSUE', '2026-04-12 14:00:00', 1),
(3, 7, 9, 'RETURN', '2026-04-25 15:00:00', 1);

-- Late fine for loan 7 (10 days late @ $4 = $40)
INSERT INTO fines (fine_id, loan_id, user_id, fine_type, assessed_at, due_date, amount, amount_paid, status, remarks) VALUES
(3, 7, 5, 'LATE_RETURN', '2026-04-25 12:05:00', '2026-05-25', 40.00, 40.00, 'PAID', '10 days late return fine');

INSERT INTO fine_payments (payment_id, fine_id, paid_at, amount, payment_method, received_by_librarian_id, receipt_no) VALUES
(3, 3, '2026-04-30 16:15:00', 40.00, 'CARD', 2, 'REC-2026-003');

INSERT INTO library_account_ledger (entry_date, entry_type, amount, reference_table, reference_id, description) VALUES
('2026-04-30 16:15:00', 'FINE_COLLECTED', 40.00, 'fine_payments', 3, 'Late fee collected Card user 5');

-- --- MAY 2026 (Current Month - Contains active / overdue checkouts) ---
INSERT INTO loan_transactions (loan_id, copy_id, borrower_user_id, issued_by_librarian_id, issued_at, due_at, returned_at, returned_by_librarian_id, issue_condition, status) VALUES
(10, 1, 3, 1, '2026-05-01 10:00:00', '2026-05-15 17:00:00', NULL, NULL, 'GOOD', 'OVERDUE'),
(11, 4, 4, 1, '2026-05-02 11:00:00', '2026-05-16 17:00:00', NULL, NULL, 'FAIR', 'OVERDUE'),
(12, 5, 5, 2, '2026-05-05 14:00:00', '2026-05-19 17:00:00', NULL, NULL, 'GOOD', 'ISSUED');

INSERT INTO book_ledger_entries (book_id, copy_id, loan_id, entry_type, entry_date, quantity) VALUES
(1, 1, 10, 'ISSUE', '2026-05-01 10:00:00', 1),
(2, 4, 11, 'ISSUE', '2026-05-02 11:00:00', 1),
(2, 5, 12, 'ISSUE', '2026-05-05 14:00:00', 1);

-- Fine issued for active overdue entry (Assessed mid-month, partial payment made)
INSERT INTO fines (fine_id, loan_id, user_id, fine_type, assessed_at, due_date, amount, amount_paid, status, remarks) VALUES
(4, 10, 3, 'LATE_RETURN', '2026-05-16 09:00:00', '2026-06-16', 30.00, 10.00, 'PARTIALLY_PAID', 'First week overdue notice calculation');

INSERT INTO fine_payments (payment_id, fine_id, paid_at, amount, payment_method, received_by_librarian_id, receipt_no) VALUES
(4, 4, '2026-05-18 13:00:00', 10.00, 'UPI', 1, 'REC-2026-004');

INSERT INTO library_account_ledger (entry_date, entry_type, amount, reference_table, reference_id, description) VALUES
('2026-05-18 13:00:00', 'FINE_COLLECTED', 10.00, 'fine_payments', 4, 'Partial payment fine installment');


-- ------------------------------------------------------------
-- 4) FINANCIAL BALANCE SHEET UPDATES
-- ------------------------------------------------------------
-- This synchronizes user account dashboard tables with transactional historical events executed above
INSERT INTO user_accounts (user_id, opening_balance, total_fines_assessed, total_payments_received, total_waived, current_balance) VALUES
(3, 0.00, 65.00, 45.00, 0.00, 20.00), -- $35 damage paid, $30 fine ($10 paid, $20 due)
(4, 0.00, 50.00, 50.00, 0.00, 0.00),  -- $50 late fine fully paid
(5, 0.00, 40.00, 40.00, 0.00, 0.00);  -- $40 late fine fully paid