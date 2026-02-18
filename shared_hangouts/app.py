from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_socketio import SocketIO
import os
from database import init_db, add_event, get_events, delete_event

app = Flask(__name__)
app.secret_key = "supersecretkey"
socketio = SocketIO(app, cors_allowed_origins="*")

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
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

        socketio.emit("new_event", {
            "name": name,
            "date": date,
            "time": time,
            "location": location,
            "notes": notes
        })

        flash("Hangout scheduled <3")
        return redirect(url_for("index"))

    events = get_events()
    return render_template("index.html", events=events)

@app.route("/delete/<int:event_id>", methods=["POST"])
def delete(event_id):
    delete_event(event_id)
    socketio.emit("delete_event", {"id": event_id})
    flash("Event deleted.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)