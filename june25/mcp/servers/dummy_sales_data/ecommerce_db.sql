--
-- E-commerce Database Schema with Sample Data
--
-- This SQL script creates a sample e-commerce database with tables for
-- categories, products, users, orders, and order items.
-- It also populates these tables with sample data.
--

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS genaicommerce;

-- Use the newly created database
USE genaicommerce;

-- Drop existing tables if they exist to ensure a clean start
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;

--
-- Table structure for `users`
--
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL, -- In a real app, store hashed passwords
    email VARCHAR(100) NOT NULL UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    zip_code VARCHAR(10),
    country VARCHAR(50),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--
-- Table structure for `categories`
--
CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

--
-- Table structure for `products`
--
CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    category_id INT,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL
);

--
-- Table structure for `orders`
--
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    status ENUM('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled') NOT NULL DEFAULT 'Pending',
    shipping_address TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

--
-- Table structure for `order_items`
--
CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL, -- Price at the time of order
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
);

--
-- Sample Data Insertion
--

-- Insert data into `users`
INSERT INTO users (username, password_hash, email, first_name, last_name, address, city, state, zip_code, country) VALUES
('john_doe', 'hashed_password_1', 'john.doe@example.com', 'John', 'Doe', '123 Main St', 'Anytown', 'CA', '90210', 'USA'),
('jane_smith', 'hashed_password_2', 'jane.smith@example.com', 'Jane', 'Smith', '456 Oak Ave', 'Otherville', 'NY', '10001', 'USA'),
('alice_wonder', 'hashed_password_3', 'alice.wonder@example.com', 'Alice', 'Wonder', '789 Pine Ln', 'Wonderland', 'FL', '33101', 'USA');

-- Insert data into `categories`
INSERT INTO categories (name, description) VALUES
('Electronics', 'Gadgets, devices, and electronic accessories.'),
('Books', 'Fiction, non-fiction, and educational books.'),
('Home & Kitchen', 'Appliances, decor, and kitchenware.'),
('Apparel', 'Clothing, shoes, and accessories.');

-- Insert data into `products`
INSERT INTO products (name, description, price, stock_quantity, category_id, image_url) VALUES
('Laptop Pro X', 'Powerful laptop for professionals.', 1200.00, 50, (SELECT category_id FROM categories WHERE name = 'Electronics'), 'https://placehold.co/600x400/000000/FFFFFF?text=Laptop'),
('The Great Novel', 'A captivating story of adventure.', 25.50, 150, (SELECT category_id FROM categories WHERE name = 'Books'), 'https://placehold.co/600x400/000000/FFFFFF?text=Book'),
('Coffee Maker Deluxe', 'Automatic coffee maker with grinder.', 89.99, 75, (SELECT category_id FROM categories WHERE name = 'Home & Kitchen'), 'https://placehold.co/600x400/000000/FFFFFF?text=Coffee+Maker'),
('Wireless Headphones', 'Noise-cancelling over-ear headphones.', 199.00, 100, (SELECT category_id FROM categories WHERE name = 'Electronics'), 'https://placehold.co/600x400/000000/FFFFFF?text=Headphones'),
('Science Fiction Anthology', 'Collection of classic sci-fi stories.', 18.75, 200, (SELECT category_id FROM categories WHERE name = 'Books'), 'https://placehold.co/600x400/000000/FFFFFF?text=Sci-Fi+Book'),
('Blender Master', 'High-speed blender for smoothies and more.', 65.00, 60, (SELECT category_id FROM categories WHERE name = 'Home & Kitchen'), 'https://placehold.co/600x400/000000/FFFFFF?text=Blender'),
('Men''s T-Shirt', 'Comfortable cotton t-shirt.', 15.00, 300, (SELECT category_id FROM categories WHERE name = 'Apparel'), 'https://placehold.co/600x400/000000/FFFFFF?text=T-Shirt');

-- Insert data into `orders`
INSERT INTO orders (user_id, total_amount, status, shipping_address) VALUES
((SELECT user_id FROM users WHERE username = 'john_doe'), 1225.50, 'Delivered', '123 Main St, Anytown, CA 90210, USA'),
((SELECT user_id FROM users WHERE username = 'jane_smith'), 264.00, 'Processing', '456 Oak Ave, Otherville, NY 10001, USA'),
((SELECT user_id FROM users WHERE username = 'alice_wonder'), 89.99, 'Pending', '789 Pine Ln, Wonderland, FL 33101, USA');

-- Insert data into `order_items`
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
((SELECT order_id FROM orders WHERE user_id = (SELECT user_id FROM users WHERE username = 'john_doe') AND total_amount = 1225.50), (SELECT product_id FROM products WHERE name = 'Laptop Pro X'), 1, 1200.00),
((SELECT order_id FROM orders WHERE user_id = (SELECT user_id FROM users WHERE username = 'john_doe') AND total_amount = 1225.50), (SELECT product_id FROM products WHERE name = 'The Great Novel'), 1, 25.50),
((SELECT order_id FROM orders WHERE user_id = (SELECT user_id FROM users WHERE username = 'jane_smith') AND total_amount = 264.00), (SELECT product_id FROM products WHERE name = 'Wireless Headphones'), 1, 199.00),
((SELECT order_id FROM orders WHERE user_id = (SELECT user_id FROM users WHERE username = 'jane_smith') AND total_amount = 264.00), (SELECT product_id FROM products WHERE name = 'Science Fiction Anthology'), 2, 18.75),
((SELECT order_id FROM orders WHERE user_id = (SELECT user_id FROM users WHERE username = 'alice_wonder') AND total_amount = 89.99), (SELECT product_id FROM products WHERE name = 'Coffee Maker Deluxe'), 1, 89.99);

--
-- End of SQL Script
--
