import sqlite3

DB_NAME = "deadlines.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deadlines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class TEXT NOT NULL,
            start TIMESTAMP NOT NULL,
            due TIMESTAMP NOT NULL,
            link TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_deadline(name, class_name, start, due, link=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO deadlines (name, class, start, due, link) VALUES (?, ?, ?, ?, ?)",
        (name, class_name, start, due, link),
    )
    conn.commit()
    conn.close()


def get_all_deadlines():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, class, start, due, link FROM deadlines ORDER BY due"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_deadline(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM deadlines WHERE id = ?", (id,))
    conn.commit()
    conn.close()
