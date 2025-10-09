#!/usr/bin/env python3
"""
Task 1: Reusable Query Executor

Simple function that executes SQL queries using the DatabaseConnection context manager.
"""

import sqlite3


class DatabaseConnection:
    """Simple context manager for database connections"""

    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Enter the context - open connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context - close connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


def execute_query(query, params=None):
    """
    Execute a SQL query using the DatabaseConnection context manager.

    Args:
        query (str): SQL query to execute
        params (tuple): Optional parameters for the query

    Returns:
        list: Query results
    """
    with DatabaseConnection() as cursor:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()


# Create sample database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        age INTEGER
    )
""")

# Insert sample data
cursor.execute(
    "INSERT OR REPLACE INTO users (id, name, email, age) VALUES (1, 'John Doe', 'john@example.com', 25)"
)
cursor.execute(
    "INSERT OR REPLACE INTO users (id, name, email, age) VALUES (2, 'Jane Smith', 'jane@example.com', 30)"
)
cursor.execute(
    "INSERT OR REPLACE INTO users (id, name, email, age) VALUES (3, 'Bob Johnson', 'bob@example.com', 35)"
)

conn.commit()
conn.close()

# Test the query executor
print("=== Task 1: Reusable Query Executor ===\n")

# Test 1: Select all users
print("1. Select all users:")
results = execute_query("SELECT * FROM users")
for row in results:
    print(f"  {row}")

# Test 2: Select users with age > 30
print("\n2. Select users with age > 30:")
results = execute_query("SELECT * FROM users WHERE age > ?", (30,))
for row in results:
    print(f"  {row}")

# Test 3: Count users
print("\n3. Count users:")
results = execute_query("SELECT COUNT(*) FROM users")
print(f"  Total users: {results[0][0]}")

print("\n=== Task 1 Complete ===")
