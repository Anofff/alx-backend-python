#!/usr/bin/env python3
"""
Task 2: Concurrent Asynchronous Database Queries

Run multiple database queries concurrently using asyncio.gather.
"""

import asyncio
import aiosqlite
import sqlite3


# Create sample database with age column
def create_sample_db():
    """Create sample database for async operations"""
    conn = sqlite3.connect("concurrent_users.db")
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


async def async_fetch_users():
    """Fetch all users from database"""
    async with aiosqlite.connect("concurrent_users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("All users fetched:")
            for row in results:
                print(row)
            return results


async def async_fetch_older_users():
    """Fetch users older than 40"""
    async with aiosqlite.connect("concurrent_users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print("Users older than 40:")
            for row in results:
                print(row)
            return results


async def fetch_concurrently():
    """Use asyncio.gather to execute both queries concurrently"""
    print("Running concurrent async database queries:")
    print("-" * 40)

    # Execute both queries concurrently using asyncio.gather
    results = await asyncio.gather(async_fetch_users(), async_fetch_older_users())

    print("\nConcurrent execution complete!")
    print(f"Total users: {len(results[0])}")
    print(f"Users older than 40: {len(results[1])}")

    return results


# Create sample database
create_sample_db()

# Run the concurrent fetch using asyncio.run
asyncio.run(fetch_concurrently())
