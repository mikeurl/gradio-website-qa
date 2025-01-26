import sqlite3
from datetime import datetime, timedelta

# Database file name
db_file = "website_cache.db"

# Create and initialize the database
def initialize_database():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        # Create a table for website content
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS website_content (
            url TEXT PRIMARY KEY,
            content TEXT,
            timestamp DATETIME
        )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")

# Store website content in the database
def store_content(url, content):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        timestamp = datetime.now()
        cursor.execute('''
        INSERT OR REPLACE INTO website_content (url, content, timestamp) VALUES (?, ?, ?)
        ''', (url, content, timestamp))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"An error occurred while storing content: {e}")

# Retrieve website content from the database
def retrieve_content(url, max_age_minutes=60):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT content, timestamp FROM website_content WHERE url = ?
        ''', (url,))
        result = cursor.fetchone()
        conn.close()
        # Check if content is found and is within the acceptable age
        if result:
            content, timestamp = result
            timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
            if datetime.now() - timestamp < timedelta(minutes=max_age_minutes):
                return content
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving content: {e}")
    return None

# Initialize the database
initialize_database()
