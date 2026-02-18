import sqlite3

DB_NAME = "events.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            location TEXT,
            notes TEXT,
            sender TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_event(name, date, time, location, notes, sender):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO events (name, date, time, location, notes, sender) VALUES (?, ?, ?, ?, ?, ?)",
        (name, date, time, location, notes, sender)
    )
    conn.commit()
    conn.close()

def get_events():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, name, date, time, location, notes, sender FROM events ORDER BY date, time")
    events = c.fetchall()
    conn.close()
    return events