from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostCreate(BaseModel):
    text: constr(max_length=1000000)

class PostDelete(BaseModel):
    post_id: int