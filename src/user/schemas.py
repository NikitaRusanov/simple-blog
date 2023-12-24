from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int


class UserDTO(UserBase):
    password: str
    id: int
