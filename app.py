from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = "subaru.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
        """)
        conn.commit()

@app.route("/")
def index():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("SELECT id, title FROM posts ORDER BY id DESC")
        posts = c.fetchall()
    return render_template("index.html", posts=posts)

@app.route("/post", methods=["GET", "POST"])
def post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        with sqlite3.connect(DB) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
            conn.commit()

        return redirect(url_for("index"))

    return render_template("post.html")

@app.route("/view/<int:post_id>")
def view(post_id):
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute("SELECT title, content FROM posts WHERE id=?", (post_id,))
        post = c.fetchone()

    return render_template("view.html", post=post)

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)