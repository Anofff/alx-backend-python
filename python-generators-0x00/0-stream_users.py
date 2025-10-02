#!/usr/bin/python3
import seed

def stream_users():
    """Generator that streams rows one by one from the user_data table"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)  # fetch rows as dictionaries
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()
