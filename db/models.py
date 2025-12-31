from sqlalchemy import String, BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from db.utils import Base
from db.utils import Model


class User(Model):
    id = None
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True,autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=True)

    @staticmethod
    async def check_user(data: dict):
        query: User | None = await User.get(user_id=data.get('user_id'))
        if not query:
            await User.create(**data)

    def __str__(self):
        return self.username


metadata = Base.metadata
