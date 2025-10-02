import random
import string
import tkinter as tk
from tkinter import filedialog

# Create the main window
window = tk.Tk()
window.title("Cipher Tool")
window.geometry("800x800")
window.resizable(False, False)
window.configure(bg="white")

# Add a label and instructions
label = tk.Label(window, text="This is a cipher tool",
                 font="Arial,20", bg="white")
instructions_label = tk.Label(
    window,
    text="This tool allows you to encrypt and decrypt messages using a simple substitution cipher.\nWhenever you're ready, press 'Encrypt'.",
    font="Arial,20",
    bg="white",
    wraplength=800,
    justify="center"
)

label.pack(pady=20, padx=20)
instructions_label.pack(pady=10, padx=10)

# Add a text box for input
text_boxin = tk.Text(window, width=25, bg="lightgrey", font="Arial,12")
text_boxin.pack(padx=10, pady=10, side=tk.LEFT)

# Add a text box for output
text_boxout = tk.Text(window, width=25, bg="lightgrey", font="Arial,12")
text_boxout.pack(padx=10, pady=10, side=tk.RIGHT)

# Save to file


def save_to_file():
    file = filedialog.asksaveasfile(defaultextension=".txt")
    file.write(text_boxout.get("1.0", tk.END))
    file.close()

# Key generation


def generate_key():
    chars = string.ascii_letters + string.digits + string.punctuation + ' '
    chars = list(chars)
    random.shuffle(chars)
    return ''.join(chars)


key = generate_key()

# Pure encryption/decryption functions (no Tkinter stuff inside)


def encrypt_message(message, key):
    encrypted = ""
    for char in message:
        if char in key:
            encrypted += key[(key.index(char) + 5) % len(key)]
        else:
            encrypted += char
    return encrypted


def decrypt_message(message, key):
    decrypted = ""
    for char in message:
        if char in key:
            decrypted += key[(key.index(char) - 5) % len(key)]
        else:
            decrypted += char
    return decrypted


def open_new_window():
    new_window = tk.Toplevel(window)
    new_window.title("New Window")
    new_window.geometry("400x400")
    new_window.configure(bg="white")
    new_label = tk.Label(
        new_window, text="Insert your key here:", font="Arial,20", bg="white")
    new_label.pack(pady=20, padx=20)

    key_entry = tk.Entry(new_window, font="Arial,20", bg="lightgrey")
    key_entry.pack(pady=10, padx=10)

    def on_submit():
        global key
        key = key_entry.get()
        new_window.destroy()

    submit_button = tk.Button(
        new_window, text="Submit", command=on_submit, font="Arial,12", bg="white")
    submit_button.pack(pady=10)

# Button handlers


def on_encrypt():
    text = text_boxin.get("1.0", tk.END).strip()
    text_boxin.delete("1.0", tk.END)
    encrypted = encrypt_message(text, key)
    text_boxout.delete("1.0", tk.END)
    text_boxout.insert(tk.END, encrypted + f"\n\nKey: {key}")


def on_decrypt():
    text = text_boxout.get("1.0", tk.END).strip()
    text_boxout.delete("1.0", tk.END)
    decrypted = decrypt_message(text, key)
    text_boxin.delete("1.0", tk.END)
    text_boxin.insert(tk.END, decrypted)


def clear_text_boxes():
    text_boxin.delete("1.0", tk.END)
    text_boxout.delete("1.0", tk.END)


# Buttons
encrypt_button = tk.Button(window, command=on_encrypt,
                           text="Encrypt", font="Arial, 12", bg="white")
encrypt_button.pack(side=tk.TOP, pady=10)

decrypt_button = tk.Button(window, command=on_decrypt,
                           text="Decrypt", font="Arial, 12", bg="white")
decrypt_button.pack(side=tk.BOTTOM, pady=10)

set_key_button = tk.Button(
    window, command=open_new_window, text="Set Key", font="Arial, 12", bg="white")
set_key_button.pack(pady=10)
clear_button = tk.Button(window, command=clear_text_boxes,
                         text="Clear", font="Arial, 12", bg="white")
clear_button.pack(pady=10)

save_button = tk.Button(window, command=save_to_file,
                        text="Save to File", font="Arial, 12", bg="white")
save_button.pack(pady=10)
window.mainloop()
