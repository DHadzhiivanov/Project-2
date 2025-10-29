import random
import string

CHARSET = string.ascii_letters + string.digits + string.punctuation


def generate_key() -> str:
    chars = list(CHARSET)
    random.shuffle(chars)
    return ''.join(chars)


def _maps(key: str):
    if not isinstance(key, str) or len(key) != len(CHARSET):
        raise ValueError("bad key")
    enc = {a: b for a, b in zip(CHARSET, key)}
    dec = {b: a for a, b in zip(CHARSET, key)}
    return enc, dec


def encrypt_text(text: str, key: str) -> str:
    enc, _ = _maps(key)
    return ''.join(enc.get(ch, ch) for ch in text)


def decrypt_text(text: str, key: str) -> str:
    _, dec = _maps(key)
    return ''.join(dec.get(ch, ch) for ch in text)
