#!/usr/bin/env python3
"""
Task 1: Reusable Query Context Manager

Create a reusable context manager that takes a query as input and executes it,
managing both connection and the query execution.
"""

import sqlite3


class ExecuteQuery:
    """Reusable context manager for executing queries"""

    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Enter the context - open connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the context - close connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        """Execute the query and store results"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.results = self.cursor.fetchall()
        return self.results


# Create sample database with age column
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table with age column
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        age INTEGER
    )
""")

# Insert sample data with ages
cursor.execute(
    "INSERT OR REPLACE INTO users (id, name, email, age) VALUES (1, 'John Doe', 'john@example.com', 25)"
)
cursor.execute(
    "INSERT OR REPLACE INTO users (id, name, email, age) VALUES (2, 'Jane Smith', 'jane@example.com', 30)"
)
cursor.execute(
    "INSERT OR REPLACE INTO users (id, name, email, age) VALUES (3, 'Bob Johnson', 'bob@example.com', 45)"
)
cursor.execute(
    "INSERT OR REPLACE INTO users (id, name, email, age) VALUES (4, 'Alice Brown', 'alice@example.com', 28)"
)
cursor.execute(
    "INSERT OR REPLACE INTO users (id, name, email, age) VALUES (5, 'Charlie Wilson', 'charlie@example.com', 50)"
)

conn.commit()
conn.close()

# Use ExecuteQuery context manager with the specified query and parameter
with ExecuteQuery() as executor:
    query = "SELECT * FROM users WHERE age > ?"
    parameter = 25
    results = executor.execute_query(query, (parameter,))
    print("Query results:")
    for row in results:
        print(row)
