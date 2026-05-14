-- library.sql

-- Create database
CREATE DATABASE IF NOT EXISTS library;

-- Use database
USE library;

-- Drop tables if they already exist
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS books;

-- Create books table
CREATE TABLE books (
    id VARCHAR(10) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    published_year INT,
    available_copies INT NOT NULL,
    total_copies INT NOT NULL,
    genre VARCHAR(100),
    available BOOLEAN DEFAULT TRUE,
    active BOOLEAN DEFAULT TRUE,
    tags JSON,
    isbn VARCHAR(20) UNIQUE
);

-- Create students table
CREATE TABLE students (
    id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    major VARCHAR(100),
    year INT,
    books_borrowed JSON,
    active BOOLEAN DEFAULT TRUE
);

-- Insert books
INSERT INTO books (
    id, title, author, published_year,
    available_copies, total_copies,
    genre, available, active, tags, isbn
) VALUES
(
    'B001',
    'The C Programming Language',
    'Brian W. Kernighan, Dennis M. Ritchie',
    1978,
    2,
    10,
    'Programming',
    TRUE,
    TRUE,
    JSON_ARRAY('programming', 'C', 'beginner'),
    '9780131103627'
),
(
    'B002',
    'Clean Code',
    'Robert C. Martin',
    2008,
    4,
    8,
    'Software Engineering',
    TRUE,
    TRUE,
    JSON_ARRAY('clean-code', 'best-practices', 'software-engineering'),
    '9780132350884'
),
(
    'B003',
    'Introduction to Algorithms',
    'Thomas H. Cormen',
    2009,
    1,
    5,
    'Algorithms',
    TRUE,
    TRUE,
    JSON_ARRAY('algorithms', 'data-structures', 'cs-core'),
    '9780262033848'
),
(
    'B004',
    'Design Patterns',
    'Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides',
    1994,
    3,
    6,
    'Software Design',
    TRUE,
    TRUE,
    JSON_ARRAY('design-patterns', 'oop', 'architecture'),
    '9780201633610'
),
(
    'B005',
    'Python Crash Course',
    'Eric Matthes',
    2019,
    5,
    10,
    'Programming',
    TRUE,
    TRUE,
    JSON_ARRAY('python', 'beginner', 'hands-on'),
    '9781593279288'
);

-- Insert students
INSERT INTO students (
    id, name, email, major,
    year, books_borrowed, active
) VALUES
(
    'S001',
    'Rahul Sharma',
    'rahul.sharma@example.com',
    'Computer Science',
    2,
    JSON_ARRAY('B001', 'B002'),
    TRUE
),
(
    'S002',
    'Priya Reddy',
    'priya.reddy@example.com',
    'Software Engineering',
    3,
    JSON_ARRAY('B003', 'B004', 'B005'),
    TRUE
),
(
    'S003',
    'Arjun Patel',
    'arjun.patel@example.com',
    'Data Science',
    1,
    JSON_ARRAY('B006', 'B007'),
    TRUE
),
(
    'S004',
    'Sneha Verma',
    'sneha.verma@example.com',
    'Artificial Intelligence',
    4,
    JSON_ARRAY('B008', 'B009', 'B010'),
    TRUE
),
(
    'S005',
    'Kiran Kumar',
    'kiran.kumar@example.com',
    'Cybersecurity',
    2,
    JSON_ARRAY('B011', 'B012'),
    TRUE
);