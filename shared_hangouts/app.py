from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_socketio import SocketIO
import os
import requests
from database import init_db, add_event, get_events

app = Flask(__name__)
app.secret_key = "supersecretkey"
socketio = SocketIO(app, cors_allowed_origins="*")  # Real-time notifications

# Initialize database
init_db()

# Replace with your girlfriend's Render URL + /receive_event
OTHER_PERSON_URL = "https://YOUR_GIRLFRIEND_RENDER_URL/receive_event"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        date = request.form.get("date")
        time = request.form.get("time")
        location = request.form.get("location")
        notes = request.form.get("notes")

        if not name or not date or not time:
            flash("Name, date, and time are required!")
            return redirect(url_for("index"))

        event = {
            "name": name,
            "date": date,
            "time": time,
            "location": location,
            "notes": notes,
            "sender": "You"
        }

        # Save locally
        add_event(event['name'], event['date'], event['time'], event['location'], event['notes'], event['sender'])

        # Send to the other person
        try:
            requests.post(OTHER_PERSON_URL, json=event)
        except Exception as e:
            flash(f"Could not send event to the other person: {e}")

        flash("Event scheduled!")
        return redirect(url_for("index"))

    events = get_events()
    return render_template("index.html", events=events)

@app.route("/receive_event", methods=["POST"])
def receive_event():
    event = request.json
    add_event(event['name'], event['date'], event['time'], event['location'], event['notes'], event.get('sender', 'Other'))
    socketio.emit('new_event', event)  # Real-time notification
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)