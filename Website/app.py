from flask import Flask, render_template, request
from encryption import generate_key, encrypt_message, decrypt_message

app = Flask(__name__)

key = generate_key()


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


if __name__ == "__main__":
    app.run(debug=True)
