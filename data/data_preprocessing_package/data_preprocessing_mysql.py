# Import necessary libraries
import pandas as pd
import pymysql
import mysql.connector
from mysql.connector import Error
from getpass import getpass
from pymysql import MySQLError
import random
from datetime import datetime, timedelta

# TODO: 1. Establish a connection to the MySQL server
# - Handle exceptions for connection errors
# - Create a new database called 'customer_analysis_db' if it doesn't exist

# TODO: 2. Create the necessary tables with appropriate relationships
# - Use SQL queries to define the 'Customers', 'Transactions', 'Products', and 'TransactionDetails' tables
# - Ensure primary and foreign keys are set correctly

# TODO: 3. Load and preprocess the dataset(s)
# - the data is not provided in the snippet, but you can assume the following steps:
# - Load 'customers.csv', 'transactions.csv', and 'products.csv' into pandas DataFrames
# - Handle missing values and ensure data types match the MySQL table schema

# TODO: 4. Insert preprocessed data into the MySQL tables
# - Insert data into the 'Customers', 'Transactions', and 'Products' tables
# - Populate the 'TransactionDetails' table with transaction-product mappings

# TODO: 5. Retrieve and verify data from the database
# - Execute SQL queries to join tables and display meaningful insights (e.g., total spending per customer)
# - Handle exceptions for query execution errors

# TODO: 6. Close the database connection
# - Ensure the connection is closed properly, even if an error occurs


# Function to establish a connection to the MySQL server
def create_connection(database_name='customer_analysis_db'):
    try:
        connection = pymysql.connect(
            host='localhost',
            user=input("Enter username: "),
            password=getpass("Enter password: "),
            database=database_name
        )
        print("Connection to MySQL established successfully.")
        return connection
    except MySQLError as e:
        print(f"Error: '{e}'")
        return None
    
# Function to create a new database if it doesn't exist
def create_database(connection, database_name='customer_analysis_db'):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Database '{database_name}' created successfully (or already exists).")
    except MySQLError as e:
        print(f"Error: '{e}'")

# Function to create tables in the database
def create_tables(connection):
    try:
        cursor = connection.cursor()
        create_customers_table = """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            email VARCHAR(100) NOT NULL,
            signup_date DATE NOT NULL
        );
        """
        create_transactions_table = """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            transaction_date DATE NOT NULL,
            total_amount FLOAT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
        """
        create_products_table = """
        CREATE TABLE IF NOT EXISTS products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(100) NOT NULL,
            category VARCHAR(100) NOT NULL,
            price FLOAT NOT NULL
        );
        """
        create_transaction_details_table = """
        CREATE TABLE IF NOT EXISTS transaction_details (
            transaction_id INT,
            product_id INT,
            quantity INT NOT NULL,
            subtotal FLOAT NOT NULL,
            FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        """
        cursor.execute(create_customers_table)
        cursor.execute(create_transactions_table)
        cursor.execute(create_products_table)
        cursor.execute(create_transaction_details_table)
        print("Tables created successfully (or already exist).")
    except MySQLError as e:
        print(f"Error: '{e}'")



# Populate the tables with data
# Note: This is a simplified example and may need to be adapted based on the actual data structure and content.




# Insert data into the Customers table
def populate_customers(cursor):
    customers = [
        ("Alice Johnson", 28, "alice@example.com", "2022-01-15"),
        ("Bob Smith", 35, "bob@example.com", "2021-11-10"),
        ("Charlie Brown", 45, "charlie@example.com", "2023-02-20"),
        # Add more customers as needed...
    ]
    insert_query = "INSERT INTO customers (name, age, email, signup_date) VALUES (%s, %s, %s, %s)"
    cursor.executemany(insert_query, customers)

# Insert data into the Transactions table
def populate_transactions(cursor):
    cursor.execute("SELECT customer_id FROM customers")
    customer_ids = [row[0] for row in cursor.fetchall()]

    transactions = [
        (customer_ids[0], "2022-01-20", 1200.00),
        (customer_ids[1], "2021-12-05", 45.99),
        (customer_ids[2], "2023-02-25", 800.00),
    ]
    insert_query = "INSERT INTO transactions (customer_id, transaction_date, total_amount) VALUES (%s, %s, %s)"
    cursor.executemany(insert_query, transactions)


# Insert data into the Products table
def populate_products(cursor):
    products = [
        ("Laptop", "Electronics", 1200.00),
        ("Python Book", "Books", 45.99),
        ("Smartphone", "Electronics", 800.00),
        # Add more products as needed...
    ]
    insert_query = "INSERT INTO products (product_name, category, price) VALUES (%s, %s, %s)"
    cursor.executemany(insert_query, products)

# Generate and insert data into Transactions and TransactionDetails tables
def populate_transactions_and_details(cursor):
    cursor.execute("SELECT customer_id FROM customers")
    customer_ids = [row[0] for row in cursor.fetchall()]  # Fetch customer_ids from the database

    cursor.execute("SELECT product_id FROM products")
    product_ids = [row[0] for row in cursor.fetchall()]  # Fetch product_ids from the database

    for customer_id in customer_ids:
        for _ in range(random.randint(1, 5)):  # Each customer makes 1-5 transactions
            transaction_date = datetime.now() - timedelta(days=random.randint(1, 365))
            total_amount = 0

            # Insert transaction
            insert_transaction = "INSERT INTO transactions (customer_id, transaction_date, total_amount) VALUES (%s, %s, %s)"
            cursor.execute(insert_transaction, (customer_id, transaction_date, total_amount))
            transaction_id = cursor.lastrowid

            # Insert transaction details (purchased products)
            products_bought = random.sample(product_ids, random.randint(1, 3))  # Buy 1-3 random products
            for product_id in products_bought:
                quantity = random.randint(1, 3)
                subtotal = quantity * 50  # Replace with actual product price lookup
                total_amount += subtotal

                # Insert transaction detail
                insert_detail = "INSERT INTO transaction_details (transaction_id, product_id, quantity, subtotal) VALUES (%s, %s, %s, %s)"
                cursor.execute(insert_detail, (transaction_id, product_id, quantity, subtotal))

            # Update transaction's total amount
            cursor.execute("UPDATE transactions SET total_amount = %s WHERE transaction_id = %s", (total_amount, transaction_id))

# function to normalise the data for a given pandas dataframe and column
def normalise_data(data_frame, column_name):
    try:
        # normalise the data
        max_value = data_frame[column_name].max()
        min_value = data_frame[column_name].min()
        data_frame[column_name] = (data_frame[column_name] - min_value) / (max_value - min_value)
        return data_frame
    except MySQLError as e:
        print(f"Error: '{e}'")
        return None





# Main function to connect and populate data
def main():
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Create database and tables
            create_database(connection)
            create_tables(connection)

            # Populate tables
            populate_customers(cursor)
            populate_transactions(cursor)
            populate_products(cursor)
            populate_transactions_and_details(cursor)

            # Commit changes
            connection.commit()

            # Save each table in the database as a pandas dataframe
            customers_df = pd.read_sql("SELECT * FROM customers", connection)
            transactions_df = pd.read_sql("SELECT * FROM transactions", connection)
            products_df = pd.read_sql("SELECT * FROM products", connection)
            transaction_details_df = pd.read_sql("SELECT * FROM transaction_details", connection)

            location = "C:/Users/david/BathUni/MA50290_24/practice_for_exam/data/data_frames"
            # Save the dataframes as csv files in 'location' directory
            customers_df.to_csv(f"{location}/customers.csv", index=False)
            transactions_df.to_csv(f"{location}/transactions.csv", index=False)
            products_df.to_csv(f"{location}/products.csv", index=False)
            transaction_details_df.to_csv(f"{location}/transaction_details.csv", index=False)
            


            print("Data successfully inserted and saved.")
        except MySQLError as e:
            print(f"Error: '{e}'")
            connection.rollback()
        except Exception as e:
            print(f"Unexpected error: '{e}'")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
            print("Connection closed.")



# Entry point of the script
# Call the main function
# This will connect to the MySQL server, create the database and tables, and populate them with data
if __name__ == "__main__":
    main()

