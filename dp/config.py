from sqlalchemy import create_engine
from utils.env_data import DBConfig
from sqlalchemy.orm import  DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import  insert, select, update, delete

class Base (DeclarativeBase):
    pass

class DB:
    engine = create_engine(DBConfig.DP_URL)


engine=DB.engine



SessionLocal = sessionmaker(engine)
class CRUD:

    @classmethod
    def save(cls, value):
        with SessionLocal() as session:
            query = insert(cls).values(**value)
            session.execute(query)
            session.commit()

    @classmethod
    def ups(cls, user_id: int, **new_values):
        with SessionLocal() as session:
            stmt = update(cls).where(cls.user_id == user_id).values(**new_values)
            session.execute(stmt)
            session.commit()

    @classmethod
    def dlt(cls, user_id):
        with SessionLocal() as session:
            stmt = delete(cls).where(cls.user_id == user_id)
            session.execute(stmt)
            session.commit()

    @classmethod
    def get(cls, filter_column, filter_value, *columns):
        with SessionLocal() as session:
            query = select(*columns).select_from(cls).where(filter_column == filter_value)
            result = session.execute(query).fetchone()
            if not result:
                return None
            if len(columns) == 1:
                return result[0]
            return result

    @classmethod
    def get_all(cls,*columns):
        with SessionLocal() as session:
            query = select(*columns)
            result = session.execute(query).fetchall()
            if result is None:
                return 'Error'
            return [row for row in result]

