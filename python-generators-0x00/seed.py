#!/usr/bin/python3
"""
seed.py

Prototypes required by the assignment:
- def connect_db()
- def create_database(connection)
- def connect_to_prodev()
- def create_table(connection)
- def insert_data(connection, data)

This script uses mysql-connector-python.
"""

import os
import csv
import uuid
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

load_dotenv()
def _db_config():
    """Read DB connection info from environment with sensible defaults."""
    host = os.getenv('MYSQL_HOST', 'localhost')
    user = os.getenv('MYSQL_USER', 'root')
    password = os.getenv('MYSQL_PASSWORD', '')
    port = int(os.getenv('MYSQL_PORT', 3306))
    return host, user, password, port

def connect_db():
    """Connect to MySQL server (no database). Returns connection or None."""
    host, user, password, port = _db_config()
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None

def create_database(connection):
    """Create ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        connection.commit()
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()

def connect_to_prodev():
    """Connect to the ALX_prodev database and return connection or None."""
    host, user, password, port = _db_config()
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database='ALX_prodev'
        )
        return conn
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None

def create_table(connection):
    """Create user_data table if it does not exist."""
    cursor = connection.cursor()
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) NOT NULL,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,0) NOT NULL,
            PRIMARY KEY (user_id)
        );
        """)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()

def insert_data(connection, data):
    """
    Insert data from CSV file into user_data table.
    `data` is expected to be the path to user_data.csv.
    Inserts only new rows (uses INSERT IGNORE).
    """
    cursor = connection.cursor()
    inserted = 0
    try:
        with open(data, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            sql = ("INSERT IGNORE INTO user_data (user_id, name, email, age) "
                   "VALUES (%s, %s, %s, %s)")
            for row in reader:
                uid = (row.get('user_id') or row.get('id') or '').strip()
                if not uid:
                    uid = str(uuid.uuid4())
                name = (row.get('name') or '').strip()
                email = (row.get('email') or '').strip()
                age_raw = (row.get('age') or '0').strip()
                try:
                    age = int(float(age_raw))
                except Exception:
                    age = 0
                cursor.execute(sql, (uid, name, email, age))
                inserted += cursor.rowcount
        connection.commit()
        print(f"Inserted {inserted} rows (duplicates ignored).")
    except FileNotFoundError:
        print(f"CSV file not found: {data}")
    except Error as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
