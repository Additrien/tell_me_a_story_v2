from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.models.user import User # Assuming User model is defined here

# Placeholder for get_db dependency. In a real app, this would come from app.db.session
# For SQLAlchemy, it might look like:
# from sqlalchemy.orm import Session
# from app.db.session import SessionLocal
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
# For now, a simple placeholder:
def get_db():
    # This is a placeholder. In a real FastAPI application,
    # this function would yield a database session.
    # e.g., from sqlalchemy.orm import Session
    # from app.db.session import SessionLocal
    # db = SessionLocal()
    # try:
    #   yield db
    # finally:
    #   db.close()
    yield None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login") # Adjusted tokenUrl to match potential full path

class TokenData(BaseModel):
    email: Optional[str] = None

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub") # Assuming email is stored in 'sub' claim
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    # Placeholder for fetching user from DB
    # In a real app, 'db' would be a SQLAlchemy Session or similar
    # user = db.query(User).filter(User.email == token_data.email).first()
    # For now, create a dummy user if email exists in token_data
    if token_data.email:
        # This is a placeholder user. In a real app, you would fetch from DB.
        # If user not found in DB after decoding token, it's also an error.
        user = User(id=1, email=token_data.email, hashed_password="fake_hashed_password") # Dummy user
    else:
        user = None # Should have been caught by email is None check

    if user is None:
        # This specific exception might be more for "user not found in DB"
        # The JWTError above handles bad tokens. If token is valid but user doesn't exist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, # Or 401, depending on desired behavior
            detail="User not found",
        )
    return user
