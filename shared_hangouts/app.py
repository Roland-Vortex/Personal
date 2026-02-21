import os
import psycopg2
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


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


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        title = request.form["title"]
        date = request.form["date"]
        time = request.form["time"]
        description = request.form["description"]

        cur.execute(
            "INSERT INTO plans (title, date, time, description) VALUES (%s, %s, %s, %s)",
            (title, date, time, description),
        )
        db.commit()

    cur.execute("SELECT * FROM plans ORDER BY date ASC")
    plans = cur.fetchall()

    cur.close()
    db.close()

    return render_template("dashboard.html", plans=plans)


@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM plans WHERE id = %s", (id,))
    db.commit()
    cur.close()
    db.close()
    return redirect("/dashboard")


@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    title = request.form["title"]
    date = request.form["date"]
    time = request.form["time"]
    description = request.form["description"]

    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
        UPDATE plans
        SET title=%s, date=%s, time=%s, description=%s
        WHERE id=%s
        """,
        (title, date, time, description, id),
    )
    db.commit()
    cur.close()
    db.close()

    return redirect("/dashboard")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
