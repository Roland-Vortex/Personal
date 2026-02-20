import os
from flask import Flask, render_template, request, redirect, session, jsonify
import psycopg2
from datetime import date
from pywebpush import webpush, WebPushException

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# -------------------------
# Database Connection
# -------------------------
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

# -------------------------
# Routes
# -------------------------
@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    db = get_db()
    cur = db.cursor()
    # Auto-delete past dates
    cur.execute("DELETE FROM dates WHERE date < %s", (date.today(),))
    db.commit()
    cur.execute("SELECT id, title, date FROM dates ORDER BY date ASC")
    dates = cur.fetchall()
    cur.close()
    db.close()
    return render_template('index.html', user=session['user'], dates=dates)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['user'] = username
            return redirect('/')
    return render_template('login.html')

@app.route('/add_date', methods=['POST'])
def add_date():
    title = request.form.get('title')
    date_value = request.form.get('date')
    user = session.get('user')
    if title and date_value and user:
        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO dates (user_id, title, date) VALUES (%s,%s,%s)",
                    (user, title, date_value))
        db.commit()
        cur.close()
        db.close()
        return redirect('/')
    return "Error adding date", 500

@app.route('/delete_date/<int:date_id>', methods=['POST'])
def delete_date(date_id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM dates WHERE id=%s", (date_id,))
    db.commit()
    cur.close()
    db.close()
    return redirect('/')

# Push notification route example
@app.route('/notify', methods=['POST'])
def notify():
    subscription_info = request.get_json()
    try:
        webpush(
            subscription_info=subscription_info,
            data="A new date has been added!",
            vapid_private_key=os.environ.get("VAPID_PRIVATE_KEY"),
            vapid_claims={"sub": os.environ.get("VAPID_EMAIL")}
        )
        return jsonify({"success": True})
    except WebPushException as e:
        print(e)
        return jsonify({"success": False}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
    app.run()
