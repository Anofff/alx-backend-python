# Python Generators – Streaming Data from MySQL

## 📌 Project Overview

This project is part of the ALX Backend Python track.
The goal is to practice Python generators (`yield`) for memory-efficient data streaming from a MySQL database.

We build scripts that:

- Connect to MySQL and seed a database from a CSV file
- Stream rows one by one from the database
- Process rows in batches
- Implement lazy pagination
- Perform memory-efficient aggregation without loading the entire dataset

## 📂 Project Structure

```
python-generators-0x00/
├── seed.py                 # Setup database and seed with user_data.csv
├── 0-stream_users.py       # Generator to stream users row by row
├── 1-batch_processing.py   # Stream users in batches and process them
├── 2-lazy_paginate.py      # Lazy pagination with LIMIT + OFFSET
├── 4-stream_ages.py        # Memory-efficient average age calculation
├── user_data.csv           # Sample dataset
└── README.md               # Project documentation
```

*`*-main.py` files were used only for local testing and are not graded by ALX.*

## 🛠️ Setup Instructions

### 1. Clone repo & enter directory

```bash
git clone https://github.com/<your-username>/alx-backend-python.git
cd alx-backend-python/python-generators-0x00
```

### 2. Create virtual environment & activate

```bash
python3 -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install mysql-connector-python
```

### 4. Setup MySQL database

- Ensure MySQL server is running
- Create a user and grant privileges:

```sql
CREATE USER 'alx'@'localhost' IDENTIFIED BY 'AlxPass123!';
GRANT ALL PRIVILEGES ON *.* TO 'alx'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Run the seeding script

```bash
python seed.py
```

## 🚀 Tasks

### Task 0 – Database Setup and Seeding
**File:** `seed.py`

- Connects to MySQL server
- Creates `ALX_prodev` database
- Creates `users` table with appropriate schema
- Seeds the table with data from `user_data.csv`

### Task 1 – Stream Rows One by One
**File:** `0-stream_users.py`

- Implements `stream_users()` generator function
- Yields user rows one at a time from the database
- Uses cursor to fetch rows incrementally

### Task 2 – Batch Processing
**File:** `1-batch_processing.py`

- Processes users in configurable batch sizes
- Demonstrates memory-efficient batch operations
- Suitable for large-scale data processing

### Task 3 – Lazy Loading Pagination
**File:** `2-lazy_paginate.py`

- Implements `lazy_pagination(page_size)` function
- Lazily fetches users page by page using LIMIT and OFFSET
- Efficient for web applications with paginated results

### Task 4 – Memory-Efficient Aggregation
**File:** `4-stream_ages.py`

- `stream_user_ages()` yields ages one by one
- `average_age()` computes average without loading all data into memory
- Demonstrates streaming aggregation patterns

## 🧪 Testing

Each task has a corresponding `*-main.py` file for local testing:

```bash
python 0-main.py   # Test row-by-row streaming
python 1-main.py   # Test batch processing  
python 2-main.py   # Test lazy pagination
python 4-main.py   # Test average age calculation
```

## 💡 Code Examples

### Streaming Users Generator

```python
def stream_users():
    """Stream users from database one by one"""
    conn = mysql.connector.connect(...)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    
    for row in cursor:
        yield row
    
    cursor.close()
    conn.close()
```

### Batch Processing

```python
def process_users_batch(batch_size=100):
    """Process users in batches for memory efficiency"""
    users = stream_users()
    batch = []
    
    for user in users:
        batch.append(user)
        if len(batch) >= batch_size:
            process_batch(batch)
            batch = []
    
    if batch:  # Process remaining users
        process_batch(batch)
```

### Memory-Efficient Average Calculation

```python
def average_age():
    """Calculate average age without loading all data"""
    total = 0
    count = 0
    
    for age in stream_user_ages():
        total += age
        count += 1
    
    return total / count if count > 0 else 0
```

## 📖 Key Learnings

- **Generator Functions:** Using `yield` to create memory-efficient iterators
- **Database Streaming:** Processing large datasets without loading everything into RAM
- **Batch Processing:** Handling data in chunks for optimal performance
- **Lazy Evaluation:** Deferring computation until needed
- **Resource Management:** Properly closing database connections and cursors
- **Streaming Aggregations:** Performing calculations on data streams

## 🔧 Requirements

- Python 3.8+
- MySQL 5.7+
- mysql-connector-python
- Virtual environment (recommended)

## 📝 Notes

- Generators maintain state between calls, making them ideal for streaming scenarios
- The `yield` keyword pauses function execution and returns a value
- Database cursors with `dictionary=True` return rows as dictionaries for easier access
- Always close database connections to prevent resource leaks