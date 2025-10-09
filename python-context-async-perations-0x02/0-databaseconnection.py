#!/usr/bin/env python3
"""
Simple Database Connection Context Manager
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


# Create sample database
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
""")

# Insert sample data
cursor.execute(
    "INSERT OR REPLACE INTO users (id, name, email) VALUES (1, 'John Doe', 'john@example.com')"
)
cursor.execute(
    "INSERT OR REPLACE INTO users (id, name, email) VALUES (2, 'Jane Smith', 'jane@example.com')"
)
cursor.execute(
    "INSERT OR REPLACE INTO users (id, name, email) VALUES (3, 'Bob Johnson', 'bob@example.com')"
)

conn.commit()
conn.close()

# Use the context manager
with DatabaseConnection() as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Query results:")
    for row in results:
        print(row)
