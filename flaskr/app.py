from flask import Flask, render_template, request
from encryption import generate_key, encrypt_message, decrypt_message
import sqlite3

app = Flask(__name__)

key = generate_key()

# connection = sqlite3.connect("database.db")

# cursor = connection.cursor()
# cursor.execute("""CREATE TABLE IF NOT EXISTS sensordata (
#                id INTEGER PRIMARY KEY AUTOINCREMENT,
#                name VARCHAR(100) NOT NULL  )
#                """)
# connection.close()


def init_db():
    with sqlite3.connect("database.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sensordata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)


if __name__ == "/":
    init_db()
    app.run(debug=True)


@app.route("/", methods=["GET", "POST"])
def index():
    encrypted = ""
    decrypted = ""
    message = ""
    action = ""

    if request.method == "POST":
        message = request.form.get("message", "")
        action = request.form.get("action", "")
        if action == "encrypt":
            encrypted = encrypt_message(message, key)
        elif action == "decrypt":
            decrypted = decrypt_message(message, key)
    return render_template("index.html", encrypted=encrypted, decrypted=decrypted, message=message, key=key)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        return
    return render_template("login.html")


@app.route("/register")
def register():
    if request.method == "POST":
        username = request.form("username")
        email = request.form("email")
        password = request.form("password")
        # TO DO: Save to database
        return "Registered Successfully!"
    return render_template("register.html")


@app.route("/notes")
def savednotes():

    return render_template("savednotes.html")


if __name__ == "__main__":
    app.run(debug=True)
