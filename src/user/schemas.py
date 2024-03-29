from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int


class UserUpdate(UserBase):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None
