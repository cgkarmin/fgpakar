import sqlite3
from sqlite3 import Connection
import hashlib

def get_connection() -> Connection:
    conn = sqlite3.connect('karangan.db')
    return conn

def create_user_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username: str, password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute('''
            INSERT INTO users (username, password) VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_user(username: str, password: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute('''
        SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

create_user_table()
