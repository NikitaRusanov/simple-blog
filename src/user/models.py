from sqlalchemy.orm import Mapped, mapped_column

from models import Base



class User(Base): # type: ignore
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]