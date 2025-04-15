import bcrypt
import os
import re

cost = int(os.getenv("SALT_COST"))

def hash_password(password: bytes):
    salt = bcrypt.gensalt(rounds=cost)
    hash = bcrypt.hashpw(password, salt)
    return hash, salt

def check_password(checkpassword: bytes, password: bytes, salt: bytes) -> bool:
    return bcrypt.hashpw(password, salt) == checkpassword