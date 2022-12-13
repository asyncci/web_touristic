import hashlib

def hash_password(password:str) :
    hashing = hashlib.sha256()
    last = hashing.update(bytes(password,encoding='utf8'))

    for i in range(3):
        last = hashing.hexdigest()
        last = hashing.update(bytes(last,encoding='utf8'))

    return hashing.hexdigest()
