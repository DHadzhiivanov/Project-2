from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os


def derive_key(password: str, salt: bytes, iterations: int = 200_000) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode('utf-8'))


def encrypt_message(plaintext: str, password: str) -> str:
    salt = os.urandom(16)
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    return urlsafe_b64encode(salt + nonce + ciphertext).decode('utf-8')


def decrypt_message(token_b64: str, password: str) -> str:
    token = urlsafe_b64decode(token_b64.encode('utf-8'))
    if len(token) < 16 + 12:
        raise ValueError("Invalid token")
    salt = token[:16]
    nonce = token[16:28]
    ciphertext = token[28:]
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    try:
        pt = aesgcm.decrypt(nonce, ciphertext, None)
    except InvalidTag:
        raise
    return pt.decode('utf-8')
