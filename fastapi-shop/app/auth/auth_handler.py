"""Module providing authentification handler."""

from datetime import datetime, timedelta, timezone
from fastapi import Depends, Request, HTTPException, status
from passlib.context import CryptContext
from jose import jwt, JWTError
from dependencies import get_db
from services.order_service import get_user_id as get_user_order_id
from services.order_item_service import get_user_id as get_user_order_item_id
from sqlalchemy.orm import Session
from config import settings
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Gets password hash."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies password."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    """Creates access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    auth_data = settings.auth_data
    encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
    return encode_jwt

def get_user_by_id(db: Session, user_id: int) -> User:
    """Gets user by id."""
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str) -> User:
    """Gets user by email."""
    return db.query(User).filter(User.email == email).first()

def authentificate_user(db: Session, email: str, password: str) -> (User | None):
    """Authentificates user."""
    user = get_user_by_email(db, email)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user

def get_token(request: Request) -> str:
    """Gets token."""
    token = request.cookies.get('user_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token

def get_current_user(token: str = Depends(get_token), db: Session = Depends(get_db)) -> User:
    """Gets current user."""
    try:
        auth_data = settings.auth_data
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is not valid')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User ID has not found')

    user = get_user_by_id(db, int(user_id))

    return user

def get_current_admin_user(
    current_user: User = Depends(get_current_user)) -> User:
    """Gets current user and checks if it is admin."""
    if current_user.is_admin:
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='The user is not admin')

def verify_current_user(
    user_id: int,
    current_user: User = Depends(get_current_user)):
    """Gets current user and checks if it is admin or user ids are the same."""
    if not (current_user.is_admin or current_user.user_id == user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No access')

def verify_current_user_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    """Gets current user and checks if it is admin or order user ids are the same."""
    if current_user.is_admin:
        return
    user_id = get_user_order_id(db, order_id)
    if not current_user.user_id == user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No access')

def verify_current_user_order_item(
    order_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    """Gets current user and checks if it is admin or order item user ids are the same."""
    if current_user.is_admin:
        return
    user_id = get_user_order_item_id(db, order_item_id)
    if not current_user.user_id == user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No access')
    