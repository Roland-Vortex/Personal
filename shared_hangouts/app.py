import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO
from database import get_conn, init_db
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

socketio = SocketIO(app)

# Initialize DB
init_db()

USERNAME = "EllaSamuel"
PASSWORD = "10-19-2025"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect("/home")
        else:
            return "Invalid login"
    return render_template("login.html")

@app.route("/home")
def home():
    if not session.get("logged_in"):
        return redirect("/")
    
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events ORDER BY id DESC")
    events = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("index.html", events=events)

@app.route("/add", methods=["POST"])
def add_event():
    if not session.get("logged_in"):
        return redirect("/")
    
    title = request.form["title"]

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO events (title) VALUES (%s)", (title,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect("/home")

@app.route("/delete/<int:event_id>")
def delete_event(event_id):
    if not session.get("logged_in"):
        return redirect("/")
    
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM events WHERE id=%s", (event_id,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect("/home")

if __name__ == "__main__":
    socketio.run(app)
