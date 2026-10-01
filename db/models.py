from sqlalchemy import String, BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from db.config import Base
from db.config import Model
from db.exceptions import DatabaseException, logger


class User(Model):
    id = None
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=True)

    @staticmethod
    async def check_user(data: dict):
        query: User | None = await User.get(User.user_id == data.get('user_id'))
        if not query:
            try:
                await User.create(**data)
            except DatabaseException as e:
                logger.error(msg=e)

    def __str__(self):
        return self.username


metadata = Base.metadata
