#!/usr/bin/env python3
"""
Task 2: Concurrent Asynchronous Database Operations

Simple async database operations using aiosqlite and asyncio.
"""

import asyncio
import aiosqlite
import sqlite3


# First, let's create a sample database
def create_sample_db():
    """Create sample database for async operations"""
    conn = sqlite3.connect("async_users.db")
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
    cursor.execute(
        "INSERT OR REPLACE INTO users (id, name, email, age) VALUES (4, 'Alice Brown', 'alice@example.com', 28)"
    )
    cursor.execute(
        "INSERT OR REPLACE INTO users (id, name, email, age) VALUES (5, 'Charlie Wilson', 'charlie@example.com', 42)"
    )

    conn.commit()
    conn.close()


async def async_execute_query(query, params=None):
    """
    Execute a SQL query asynchronously.

    Args:
        query (str): SQL query to execute
        params (tuple): Optional parameters for the query

    Returns:
        list: Query results
    """
    async with aiosqlite.connect("async_users.db") as db:
        async with db.execute(query, params or ()) as cursor:
            return await cursor.fetchall()


async def get_all_users():
    """Get all users from database"""
    print("Fetching all users...")
    results = await async_execute_query("SELECT * FROM users")
    print(f"Found {len(results)} users")
    return results


async def get_users_by_age(min_age):
    """Get users older than specified age"""
    print(f"Fetching users older than {min_age}...")
    results = await async_execute_query("SELECT * FROM users WHERE age > ?", (min_age,))
    print(f"Found {len(results)} users older than {min_age}")
    return results


async def get_user_count():
    """Get total user count"""
    print("Counting users...")
    results = await async_execute_query("SELECT COUNT(*) FROM users")
    count = results[0][0]
    print(f"Total users: {count}")
    return count


async def main():
    """
    Demonstrate concurrent async database operations.
    """
    print("=== Task 2: Concurrent Async Database Operations ===\n")

    # Create sample database
    create_sample_db()

    # Run multiple async operations concurrently
    print("Running concurrent async operations:")
    print("-" * 40)

    # Use asyncio.gather to run multiple operations concurrently
    results = await asyncio.gather(
        get_all_users(), get_users_by_age(30), get_user_count()
    )

    print("\nResults:")
    print("-" * 20)
    print(f"All users: {len(results[0])} found")
    print(f"Users > 30: {len(results[1])} found")
    print(f"Total count: {results[2]}")

    print("\n=== Task 2 Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
