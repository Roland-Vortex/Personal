from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO
import os
from database import init_db, add_event, get_events, delete_event

app = Flask(__name__)
app.secret_key = "supersecretkey"
socketio = SocketIO(app, cors_allowed_origins="*")

init_db()

# ---- LOGIN SETTINGS ----
USERNAME = "EllaSamuel"
PASSWORD = "10-19-2025"

# ---- LOGIN ROUTE ----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("index"))
        else:
            flash("Invalid login credentials.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

# ---- MAIN PAGE ----
@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("name")
        date = request.form.get("date")
        time = request.form.get("time")
        location = request.form.get("location")
        notes = request.form.get("notes")

        if not name or not date or not time:
            flash("Name, date, and time are required.")
            return redirect(url_for("index"))

        add_event(name, date, time, location, notes)
        socketio.emit("refresh")
        flash("Hangout scheduled 💗")
        return redirect(url_for("index"))

    events = get_events()
    return render_template("index.html", events=events)

@app.route("/delete/<int:event_id>", methods=["POST"])
def delete(event_id):
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    delete_event(event_id)
    socketio.emit("refresh")
    flash("Event deleted.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)
    socketio.run(app, host="0.0.0.0", port=port)