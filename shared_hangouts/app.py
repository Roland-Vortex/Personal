from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO
from database import get_conn, init_db
import eventlet

eventlet.monkey_patch()  # Important for Render with eventlet

app = Flask(__name__)
app.secret_key = "replace_with_a_secret_key"
socketio = SocketIO(app)

# Initialize DB
init_db()

# Hardcoded login for now
USER_CREDENTIALS = {
    "EllaSamuel": "10-19-2025"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session["user"] = username
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/home", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    conn = get_conn()
    cur = conn.cursor()
    
    if request.method == "POST":
        name = request.form.get("name")
        date = request.form.get("date")
        time = request.form.get("time")
        location = request.form.get("location")
        notes = request.form.get("notes")
        cur.execute(
            "INSERT INTO events (name, date, time, location, notes) VALUES (%s,%s,%s,%s,%s)",
            (name, date, time, location, notes)
        )
        conn.commit()
    
    cur.execute("SELECT id, name, date, time, location, notes FROM events ORDER BY date")
    events = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template("index.html", events=events)
