import hashlib
import string
import uuid


def create_password_hash_and_salt(password, salt=None):
    if password is None:
        return None, None

    if salt is None:
        salt = uuid.uuid4().hex

    pw_bytes    = password.encode('utf-8')
    salt_bytes  = salt.encode('utf-8')

    hashed_password = hashlib.sha512(pw_bytes + salt_bytes).hexdigest()

    return hashed_password, salt


def verify_password(password, hashed_password, salt):
    re_hashed, salt = create_password_hash_and_salt(password, salt)

    return re_hashed == hashed_password


def generate_password(pwd_length, symbols=string.ascii_letters + string.digits + string.digits):
    from Crypto.Random.random import StrongRandom

    ret = ""
    rnd = StrongRandom()
    for i in range(pwd_length):
        ret += rnd.choice(symbols)

    return ret
