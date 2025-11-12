import sqlite3

def create_table():
    with sqlite3.connect("users.db") as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT UNIQUE
            )
        """)
        con.commit()

def create_admin_text_table():
    with sqlite3.connect("users.db") as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS admin_text (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT UNIQUE,
                image TEXT UNIQUE
            )
        """)
        con.commit()











create_table()
create_admin_text_table()
















def add_user(user_id: int, username: str):
    with sqlite3.connect("users.db") as con:
        cursor = con.cursor()
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        cursor.close()

def get_users():
    with sqlite3.connect("users.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        return [dict(row) for row in data]

def add_text(content: str, image: str = None):
    with sqlite3.connect("users.db") as con:
        cursor = con.cursor()
        cursor.execute("UPDATE admin_text SET text=?, image=? WHERE id=1", (content, image))
        
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO admin_text (text, image) VALUES (?, ?)", (content, image))
        
        con.commit()

def get_text():
    with sqlite3.connect("users.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM admin_text")
        data = cur.fetchall()
        return [dict(row) for row in data]
