from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):

    def __repr__(self) -> str:
        cols = self.__table__.columns.keys()
        attrs = [f"{col}={getattr(self, col)}" for col in cols]

        return f"<{self.__class__.__name__}({", ".join(attrs)})>"
