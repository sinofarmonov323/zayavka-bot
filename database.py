import sqlite3

def create_table():
    with sqlite3.connect("users.db") as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                used_id INTEGER UNIQUE,
                username TEXT UNIQUE
            )
        """)
        con.commit()

create_table()

def add_user(user_id: int, username: str):
    with sqlite3.connect("users.db") as con:
        cursor = con.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (used_id, username) VALUES (?, ?)", (user_id, username))
        cursor.close()
