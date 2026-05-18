import sqlite3

db = sqlite3.connect(
    "tasks.db",
    check_same_thread=False
)

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    priority TEXT,
    status TEXT,
    due_date TEXT
)
""")

db.commit()