from datetime import datetime
from pydantic import BaseModel

class UserAuth(BaseModel):
    email: str
    password: str

class User(BaseModel):
    user_name: str
    birth_date: datetime
    sex: bool

class UserRecord(User):
    user_id: int

class UserPrivateRecord(UserRecord, UserAuth):
    is_admin: bool

class UserRegister(User, UserAuth):
    pass

class UserUpdate(User):
    pass

class UserResponse(UserRecord, UserAuth):
    pass