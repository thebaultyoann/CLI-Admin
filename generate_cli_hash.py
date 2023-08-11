from passlib.context import CryptContext
import sys

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

password = sys.argv[1] if len(sys.argv) > 1 else None  

password = get_password_hash(password)
password = get_password_hash(password)
print(password[:32])
