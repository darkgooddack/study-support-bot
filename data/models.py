from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from data.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    username: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[str] = mapped_column(nullable=True)
    direction: Mapped[str] = mapped_column(nullable=True)
    about: Mapped[str] = mapped_column(nullable=True)
    github: Mapped[str] = mapped_column(nullable=True)
    linkedin: Mapped[str] = mapped_column(nullable=True)
    visibility: Mapped[bool] = mapped_column(nullable=False, default=True)
