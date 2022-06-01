from flask import Flask, render_template, g, request, session, redirect, flash, url_for, abort
import sqlite3

DATABASE = 'database.bd'
SECRET_KEY = "key"

app = Flask(__name__)
#To use SECRET_KEY
app.config.from_object(__name__)

def connect_bd():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.bd = connect_bd()

@app.teardown_request
def after_request(e):
    g.bd.close()

@app.route("/")
def display_entries():
    sql = "SELECT title, wording, created_at FROM entries ORDER BY id DESC"
    cur = g.bd.execute(sql)
    entries = []
    for title, wording, created_at in cur.fetchall():
        entries.append({"title": title, "wording": wording, "created_at": created_at})
    return render_template("display_entries.html", entries=entries)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form['username'] == "admin" and request.form['password'] == "admin":
            session['logged'] = True
            flash("Login successful!")
            return redirect(url_for('display_entries'))
        error = "User or Password incorrect"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop('logged', None)
    flash("Logout successful!")
    return redirect(url_for('display_entries'))

@app.route("/insert", methods=["POST"])
def insert_entries():
    if not session.get('logged'):
        abort(401)
    title = request.form['title']
    wording = request.form['wording']
    sql = "INSERT INTO entries(title, wording) VALUES (?, ?)"
    g.bd.execute(sql, [title, wording])
    g.bd.commit()
    flash("New entry inserted successfully!")
    return redirect(url_for('display_entries'))

if __name__ == "__main__":
    app.run()
