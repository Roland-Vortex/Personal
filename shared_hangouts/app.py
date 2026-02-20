import os
import json
from datetime import date
from flask import Flask, render_template, request, redirect, session
import psycopg2
from pywebpush import webpush

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# Database connection
def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        port=os.environ.get("DB_PORT")
    )

# Auto delete past dates
def delete_old_dates():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM events WHERE date < CURRENT_DATE;")
    conn.commit()
    cur.close()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "EllaSamuel" and request.form["password"] == "10-19-2025":
            session["user"] = "lover"
            return redirect("/home")
    return render_template("login.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect("/")

    delete_old_dates()

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        event_date = request.form["date"]
        time = request.form["time"]
        location = request.form["location"]
        notes = request.form["notes"]

        cur.execute(
            "INSERT INTO events (title, date, time, location, notes) VALUES (%s,%s,%s,%s,%s)",
            (title, event_date, time, location, notes)
        )
        conn.commit()

    cur.execute("SELECT * FROM events ORDER BY date ASC;")
    events = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", events=events)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM events WHERE id=%s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/home")

@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE events SET title=%s, date=%s, time=%s, location=%s, notes=%s WHERE id=%s",
        (
            request.form["title"],
            request.form["date"],
            request.form["time"],
            request.form["location"],
            request.form["notes"],
            id
        )
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/home")

if __name__ == "__main__":
    app.run()