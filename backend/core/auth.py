import bcrypt
import os
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from dotenv import load_dotenv

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

def get_password_hash(password: str):
    # 1. Convert to bytes and truncate to 72
    pwd_bytes = password.encode('utf-8')[:72]
    # 2. Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    # 3. Return as string to store in MySQL
    return hashed.decode('utf-8')

def verify_password(plain_password, hashed_password):
    # 1. Convert inputs to bytes
    pwd_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    # 2. Use bcrypt's native check
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)