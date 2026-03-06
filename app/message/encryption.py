from cryptography.fernet import Fernet, InvalidToken
from flask import current_app
import os

KEY_FILE = "fernet.key"

def key_load_or_generate():
    key_path = os.path.join(current_app.instance_path, KEY_FILE)

    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            return f.read()
    
    key = Fernet.generate_key()

    os.makedirs(current_app.instance_path, exist_ok=True)

    with open(key_path, "wb") as f:
        f.write(key)

    return key

def get_fernet():
    key = current_app.config["FERNET_KEY"]

    if key:
        if isinstance(key, str):
            key = key.encode()
        return Fernet(key)
    
    key = key_load_or_generate()
    return Fernet(key)


def encrypter(msg):
    if msg is None:
        return None

    f = get_fernet()

    encrypted = f.encrypt(msg.encode()).decode()

    return encrypted

def decrypter(en_msg):
    if en_msg is None:
        return None

    f = get_fernet()
    try:
        decrypted = f.decrypt(en_msg.encode()).decode()
        return decrypted
    except InvalidToken:
        return en_msg