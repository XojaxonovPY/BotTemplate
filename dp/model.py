
from dp.config import  Base,DB,CRUD,SessionLocal
from sqlalchemy import Integer, String, ForeignKey, Text, BIGINT, TIMESTAMP, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, sessionmaker

engine=DB.engine


class User(Base, CRUD):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)

Base.metadata.create_all(engine)
metadata=Base.metadata