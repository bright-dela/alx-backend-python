import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    """Decorator that logs the SQL query before executing it"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if 'query' in kwargs:
            print(f"[{timestamp}] Executing SQL Query: {kwargs['query']}")
        elif len(args) > 0:
            print(f"[{timestamp}] Executing SQL Query: {args[0]}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
