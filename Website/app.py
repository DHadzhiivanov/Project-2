from flask import Flask, render_template, request
from encryption import generate_key, encrypt_message, decrypt_message
import sqlite3

app = Flask(__name__)

key = generate_key()

# connection = sqlite3.connect("database.db")

# cursor = connection.cursor()
# cursor.execute("""CREATE TABLE IF NOT EXISTS sensordata (
#                id INT AUTO_INCREMENT PRIMARY KEY,
#                name VARCHAR(100) NOT NULL  )
#                """)
# connection.close()


@app.route("/", methods=["GET", "POST"])
def index():
    encrypted = ""
    decrypted = ""
    message = ""
    action = ""

    # connection = sqlite3.connect('database.db')
    # cursor = connection.cursor()
    # cursor.execute("""
    #     INSERT INTO sensordata (id, name)  VALUES (NULL, 'test')
    # """)
    # connection.commit()
    # connection.close()

    # SELECT name FROM sensordata WHERE name = 'test'

    if request.method == "POST":
        message = request.form.get("message", "")
        action = request.form.get("action", "")
        if action == "encrypt":
            encrypted = encrypt_message(message, key)
        elif action == "decrypt":
            decrypted = decrypt_message(message, key)
    return render_template("index.html", encrypted=encrypted, decrypted=decrypted, message=message, key=key)


@app.route("/login")
def login():

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
