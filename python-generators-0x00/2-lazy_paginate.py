#!/usr/bin/python3
seed = __import__('seed')

def paginate_users(page_size, offset):
    """Fetch a single page of users from DB"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """Generator that yields pages lazily"""
    offset = 0
    while True:
        rows = paginate_users(page_size, offset)
        if not rows:   # stop when no more rows
            break
        yield rows
        offset += page_size
