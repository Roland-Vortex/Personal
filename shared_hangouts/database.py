import psycopg2
import os

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT", "5432")

def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            location TEXT,
            notes TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def add_event(name, date, time, location, notes):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO events (name, date, time, location, notes) VALUES (%s, %s, %s, %s, %s)",
        (name, date, time, location, notes)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_events():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, date, time, location, notes FROM events ORDER BY date, time")
    events = cur.fetchall()
    cur.close()
    conn.close()
    return events

def delete_event(event_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM events WHERE id = %s", (event_id,))
    conn.commit()
    cur.close()
    conn.close()