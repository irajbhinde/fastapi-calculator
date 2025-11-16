from passlib.hash import pbkdf2_sha256

def hash_password(plain: str) -> str:
    # pbkdf2_sha256 does not have the 72-byte bcrypt limit and needs no external backend
    return pbkdf2_sha256.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pbkdf2_sha256.verify(plain, hashed)
