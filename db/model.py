
from sqlalchemy import Text, String, BIGINT, DECIMAL, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base, db
from db.utils import CreatedModel



class User(CreatedModel):
    user_id:Mapped[int]=mapped_column(BIGINT,unique=True)
    username:Mapped[str]=mapped_column(String,nullable=True)



metadata = Base.metadata
