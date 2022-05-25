from flask import Flask, render_template, g
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
    return render_template("layout.html", entries=entries)

if __name__ == "__main__":
    app.run()
