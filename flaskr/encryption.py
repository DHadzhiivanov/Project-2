import random
import string


def generate_key():
    chars = string.ascii_letters + string.digits + string.punctuation + ' '
    chars = list(chars)
    random.shuffle(chars)
    return ''.join(chars)


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
