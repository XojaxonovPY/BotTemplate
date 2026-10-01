from datetime import datetime
from typing import TypeVar, Type, Any, Union, Sequence

from sqlalchemy import DateTime, Select, TextClause, Result, delete
from sqlalchemy import insert, update, select, text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, DataError, OperationalError
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, InstrumentedAttribute, load_only

from core.env_data import get_current_uzb_time
from db.exceptions import DatabaseException, logger
from db.session import AsyncSessionLocal

T = TypeVar("T", bound="Model")
FIELDS = Union[Sequence[str], Sequence[InstrumentedAttribute]] | None

RELATIONS = Sequence[Any] | None


class Base(DeclarativeBase):
    pass


class Manager:
    @classmethod
    def _parse_fields(cls, fields: FIELDS) -> Sequence[InstrumentedAttribute]:
        if not fields:
            return ()
        resolved = []
        for field in fields:
            if isinstance(field, str) and hasattr(cls, field):
                attr = getattr(cls, field)
                if isinstance(attr, InstrumentedAttribute):
                    resolved.append(attr)
            elif isinstance(field, InstrumentedAttribute):
                resolved.append(field)
        return tuple(resolved)

    @classmethod
    def _build_select(
            cls: Type[T],
            *filters: Any,
            fields: FIELDS = None,
            relations: RELATIONS = None,
            order_by: Sequence[Any] | None = None,
    ) -> Select[tuple[T]]:
        stmt = select(cls)

        if filters:
            stmt = stmt.where(*filters)

        selected_attrs = cls._parse_fields(fields)
        if selected_attrs:
            stmt = stmt.options(load_only(*selected_attrs))

        if relations:
            stmt = stmt.options(*relations)

        if order_by is not None:
            stmt = stmt.order_by(*order_by)

        return stmt

    @classmethod
    async def create(cls: Type[T], **values):
        async with AsyncSessionLocal() as session:
            try:
                dialect = session.bind.dialect.name
                stmt = insert(cls).values(**values)
                if dialect == "mysql":
                    res = await session.execute(stmt)
                    await session.commit()
                    return res.inserted_primary_key[0]
                else:
                    stmt = stmt.returning(cls.id)
                    res = await session.execute(stmt)
                    await session.commit()
                    return res.scalar_one()
            except SQLAlchemyError as e:
                await session.rollback()
                cls._handle_db_error(e)

    @classmethod
    async def update(cls: Type[T], *filter_, **values):
        async with AsyncSessionLocal() as session:
            try:
                query = update(cls).where(*filter_).values(**values)
                result = await session.execute(query)
                await session.commit()
                return result.rowcount()
            except(SQLAlchemyError) as e:
                await session.rollback()
                cls._handle_db_error(e)

    @classmethod
    async def delete(cls: Type[T], *filter_):
        async with AsyncSessionLocal() as session:
            try:
                query = delete(cls).where(*filter_)
                result = await session.execute(query)
                await session.commit()
                return result.rowcount()
            except(SQLAlchemyError) as e:
                await session.rollback()
                cls._handle_db_error(e)

    @classmethod
    async def get_all(
            cls: Type[T],
            *filters: Any,
            fields: FIELDS = None,
            relations: RELATIONS = None,
            order_by: Sequence[Any] | None = None,
            limit: int | None = None,
            offset: int | None = None,
    ) -> Sequence[T]:
        async with AsyncSessionLocal() as session:
            try:
                stmt = cls._build_select(
                    *filters, fields=fields, relations=relations, order_by=order_by
                )
                if limit is not None:
                    stmt = stmt.limit(limit)
                if offset is not None:
                    stmt = stmt.offset(offset)

                result = await session.execute(stmt)
                return result.scalars().all()
            except SQLAlchemyError as e:
                cls._handle_db_error(e)
                raise e

    @classmethod
    async def get(cls: Type[T], *filters: Any, fields: FIELDS = None, relations: RELATIONS = None) -> T | None:
        async with AsyncSessionLocal() as session:
            try:
                stmt = cls._build_select(
                    *filters, fields=fields, relations=relations
                )
                result = await session.execute(stmt)
                return result.scalar_one_or_none()
            except SQLAlchemyError as e:
                cls._handle_db_error(e)
                raise e

    @classmethod
    async def get_filter(cls: Type[T], *filter_, order_by_fields: list[str] = None, limit: int = 100, offset: int = 0):
        async with AsyncSessionLocal() as session:
            try:
                query: Select[Any] = select(cls).where(*filter_).limit(limit).offset(offset)
                if order_by_fields:
                    query = query.order_by(*order_by_fields)
                result: Result[Any] = await session.execute(query)
                return result.scalars().all()
            except(SQLAlchemyError) as e:
                await session.rollback()
                cls._handle_db_error(e)

    @classmethod
    async def get_query(cls: Type[T], stmt: Select[Any]):
        async with AsyncSessionLocal() as session:
            try:
                result: Result[Any] = await session.execute(stmt)
                return result
            except(SQLAlchemyError) as e:
                await session.rollback()
                cls._handle_db_error(e)

    @staticmethod
    async def core_get(query: str, **params):
        async with AsyncSessionLocal() as session:
            try:
                stmt: TextClause = text(query)
                result: Result[Any] = await session.execute(stmt, params)
                return result
            except(SQLAlchemyError) as e:
                await session.rollback()
                Manager._handle_db_error(e)

    @staticmethod
    async def core_commit(query: str, **params):
        async with AsyncSessionLocal() as session:
            try:
                stmt: TextClause = text(query)
                await session.execute(stmt, params)
                await session.commit()
            except (SQLAlchemyError) as e:
                await session.rollback()
                Manager._handle_db_error(e)

    @classmethod
    def _handle_db_error(cls, e: Exception) -> None:
        orig = getattr(e, "orig", None)
        error_msg = str(orig) if orig else str(e)

        if isinstance(e, IntegrityError):
            logger.error(e)
            raise DatabaseException(
                message=f"Integrity constraint violation: {error_msg}"
            )
        if isinstance(e, DataError):
            logger.error(e)
            raise DatabaseException(
                message="Data format error."
            )
        if isinstance(e, OperationalError):
            logger.error(e)
            raise DatabaseException(
                message="Database connection failure.",
            )
        logger.error(e)
        raise DatabaseException(
            message=f"Database error: {error_msg}"
        )


tz: str = "CURRENT_TIMESTAMP"


class Model(Base, Manager):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower() + 's'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=get_current_uzb_time())
