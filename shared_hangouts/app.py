import os
from flask import Flask, render_template, request, redirect, session
import psycopg2

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "mysecret123")

# Database connection
def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        port=os.environ.get("DB_PORT"),
        sslmode="require"
    )

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "EllaSamuel" and password == "10-19-2025":
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM dates ORDER BY date ASC;")
    dates = cur.fetchall()
    cur.close()
    db.close()

    return render_template("dashboard.html", dates=dates)

@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    date_value = request.form["date"]

    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO dates (title, date) VALUES (%s, %s);",
                (title, date_value))
    db.commit()
    cur.close()
    db.close()

    return redirect("/dashboard")

@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM dates WHERE id=%s;", (id,))
    db.commit()
    cur.close()
    db.close()

    return redirect("/dashboard")

@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    title = request.form["title"]
    date_value = request.form["date"]

    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE dates SET title=%s, date=%s WHERE id=%s;",
                (title, date_value, id))
    db.commit()
    cur.close()
    db.close()

    return redirect("/dashboard")

if __name__ == "__main__":
    app.run()