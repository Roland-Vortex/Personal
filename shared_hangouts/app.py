import os
from datetime import date
from flask import Flask, render_template, request, redirect, session, jsonify
import psycopg2
from pywebpush import webpush, WebPushException

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.debug = True

# --- Database connection ---
def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        port=os.environ.get("DB_PORT"),
        sslmode="require",
        connect_timeout=5
    )

# --- Routes ---
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")
    conn = get_db()
    cur = conn.cursor()
    # Delete past dates automatically
    cur.execute("DELETE FROM dates WHERE date_value < CURRENT_DATE")
    conn.commit()
    cur.execute("SELECT id, date_value FROM dates WHERE user_id=%s ORDER BY date_value ASC", (session["user_id"],))
    dates = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", dates=dates, theme=session.get("theme", "red"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        session["user_id"] = user_id
        session["theme"] = "red"
        return redirect("/")
    return render_template("login.html")

@app.route("/add_date", methods=["POST"])
def add_date():
    date_value = request.form.get("date")
    if not date_value:
        return "No date provided", 400
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO dates (user_id, date_value) VALUES (%s, %s)", (session["user_id"], date_value))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

@app.route("/delete_date/<int:date_id>")
def delete_date(date_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM dates WHERE id=%s AND user_id=%s", (date_id, session["user_id"]))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

@app.route("/change_theme", methods=["POST"])
def change_theme():
    new_theme = request.form.get("theme")
    session["theme"] = new_theme
    return jsonify(success=True)
