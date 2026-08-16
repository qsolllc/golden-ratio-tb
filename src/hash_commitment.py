import hashlib

def hash_bytes(data: bytes) -> str:
    return "sha3-512:" + hashlib.sha3_512(data).hexdigest()
