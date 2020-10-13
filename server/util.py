import hashlib
import uuid

def hashStr(string):
    md5 = hashlib.md5()
    md5.update(string.encode())
    return md5.hexdigest()

def gen_uuid():
    return uuid.uuid4().hex

