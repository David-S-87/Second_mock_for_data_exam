-- creating a database to understand relationships between tables

CREATE DATABASE `customer_analysis_db`;

USE `customer_analysis_db`;

-- Create the 'customers' table
-- customer_id (INT, PK), name (VARCHAR), age (INT), email (VARCHAR), signup_date (DATE)
-- customer_id is the primary key

CREATE TABLE `customers` (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(100) NOT NULL,
    signup_date DATE NOT NULL
);

-- Create the 'transactions' table
-- transaction_id (INT, PK), customer_id (INT, FK), transaction_date (DATE), total_amount (FLOAT)
-- Primary: transaction_id, Foreign: customer_id

CREATE TABLE `transactions` (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    transaction_date DATE NOT NULL,
    total_amount FLOAT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Create the 'products' table
-- product_id (INT, PK), product_name (VARCHAR), category (VARCHAR), price (FLOAT)
-- product_id is the primary key

CREATE TABLE `products` (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL
);

-- Create the 'transaction_details' table
-- transaction_id (INT, FK), product_id (INT, FK), quantity (INT), subtotal (FLOAT)
-- Foreign: transaction_id, product_id

CREATE TABLE `transaction_details` (
    transaction_id INT,
    product_id INT,
    quantity INT NOT NULL,
    subtotal FLOAT NOT NULL,
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);



