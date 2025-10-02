#!/usr/bin/python3
seed = __import__('seed')

def stream_user_ages():
    """Generator that yields ages of users one by one"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:   # each row is a tuple like (age,)
        yield age
    cursor.close()
    connection.close()


def average_age():
    """Compute average age using generator"""
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1
    avg = total / count if count > 0 else 0
    print(f"Average age of users: {avg:.2f}")
