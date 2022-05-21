from passlib.context import CryptContext



crypt = CryptContext(schemes=['bcrypt'], deprecated='auto')



def hash_password(password: str):
    return crypt.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return crypt.verify(plain_password, hashed_password)


