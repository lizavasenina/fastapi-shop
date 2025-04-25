"""Module providing auth routes."""

from fastapi import APIRouter, Depends, Response, HTTPException, status
from dependencies import get_db
from sqlalchemy.orm import Session
from services.user_service import get_user_by_email
from schemas.user import UserRegister, UserAuth, UserPrivateRecord
from models import User
from auth import auth_handler

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserPrivateRecord)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """Registers user"""
    user = get_user_by_email(db, user_data.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists'
        )
    db_user = User(user_name = user_data.user_name,
                    birth_date = user_data.birth_date,
                    sex = user_data.sex,
                    email = user_data.email,
                    password = auth_handler.get_password_hash(user_data.password))

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", status_code=status.HTTP_200_OK, response_model=dict)
def auth_user(response: Response, user_data: UserAuth, db: Session = Depends(get_db)):
    """Authentificate user"""
    check = auth_handler.authentificate_user(db, user_data.email, user_data.password)

    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Wrong email or password')

    access_token = auth_handler.create_access_token({"sub": str(check.user_id)})
    response.set_cookie(key="user_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}

@router.put("/admin/{user_id}", status_code=status.HTTP_200_OK, response_model=dict)
def make_admin(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(auth_handler.get_current_admin_user)):
    """Makes user an admin"""
    user = auth_handler.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )

    user.is_admin = True
    return { "message": "User with id {user_id} became an admin" }

@router.post("/logout", status_code=status.HTTP_200_OK, response_model=dict)
def logout_user(response: Response):
    """Logout user"""
    response.delete_cookie(key="user_access_token")
    return { "message": "User successfully log out" }
