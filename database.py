import sqlite3
from sqlite3 import Connection

def get_connection() -> Connection:
    conn = sqlite3.connect('karangan.db')
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS karangan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_tables()
