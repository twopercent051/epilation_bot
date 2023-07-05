from sqlalchemy import MetaData, DateTime, Column, Integer, String, TEXT, DATE, TIME, JSON, BOOLEAN, TIMESTAMP, select, \
    insert, delete, update, inspect
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker, as_declarative
from sqlalchemy.sql import expression

from create_bot import DATABASE_URL

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@as_declarative()
class Base:
    metadata = MetaData()


class UtcNow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(UtcNow, 'postgresql')
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class TextsDB(Base):
    """Тексты, id фоток и видео"""
    __tablename__ = "texts"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    chapter = Column(String, nullable=False)
    text = Column(TEXT, nullable=False)  # Может быть id файла


class ServicesDB(Base):
    """Перечень услуг и прайс-лист"""
    __tablename__ = "services"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    category = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)  # Время выполнения услуги в минутах
    status = Column(String, nullable=False, server_default="enabled")
    ordering = Column(Integer, nullable=False, server_default="1")


class ClientsDB(Base):
    """Профили клиентов"""
    __tablename__ = "clients"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    user_id = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    username = Column(String, nullable=False, server_default="")
    phone = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    birthday = Column(DATE, nullable=True)
    note = Column(TEXT, nullable=True)


class MailingsDB(Base):
    """Рассылки"""
    __tablename__ = "mailings"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    client_groups = Column(String, nullable=False)
    dtime = Column(TIMESTAMP, nullable=False)
    text = Column(TEXT, nullable=False)
    status = Column(String, nullable=False)


class RegistrationsDB(Base):
    """Записи клиентов"""
    __tablename__ = "registrations"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    phone = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    reg_date = Column(DATE, nullable=False)
    reg_time_start = Column(TIME, nullable=False)
    reg_time_finish = Column(TIME, nullable=False)
    services = Column(JSON, nullable=True)
    total_price = Column(Integer, nullable=True)
    is_blocked = Column(BOOLEAN, nullable=False)
    status = Column(String, nullable=False)  # created cancelled finished


class StaticsDB(Base):
    __tablename__ = "statics"

    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    category = Column(String, nullable=True)
    title = Column(String, nullable=False)
    file_id = Column(String, nullable=False)


class BaseDAO:
    """Класс взаимодействия с БД"""
    model = None

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by).limit(1)
            result = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def get_many(cls, **filter_by) -> list:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def create(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data)
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().one_or_none()

    @classmethod
    async def delete(cls, **data):
        async with async_session_maker() as session:
            stmt = delete(cls.model).filter_by(**data)
            await session.execute(stmt)
            await session.commit()


class TextsDAO(BaseDAO):
    model = TextsDB

    @classmethod
    async def update(cls, chapter: str, **data):
        async with async_session_maker() as session:
            stmt = update(cls.model).values(**data).filter_by(chapter=chapter)
            await session.execute(stmt)
            await session.commit()


class ServicesDAO(BaseDAO):
    model = ServicesDB

    @classmethod
    async def get_order_list(cls, **filter_by) -> list:
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(**filter_by).order_by(ServicesDB.ordering.asc(),
                                                                                        ServicesDB.id.asc())
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def update(cls, service_id: int, data):
        async with async_session_maker() as session:
            stmt = update(cls.model).values(data).filter_by(id=service_id)
            await session.execute(stmt)
            await session.commit()


class ClientsDAO(BaseDAO):
    model = ClientsDB


class MailingsDAO(BaseDAO):
    model = MailingsDB


class RegistrationsDAO(BaseDAO):
    model = RegistrationsDB

    @classmethod
    async def get_by_user_id(cls, user_id: str) -> dict:
        async with async_session_maker() as session:
            query_clients = select(ClientsDB.__table__.columns).filter_by(user_id=user_id).limit(1)
            result = await session.execute(query_clients)
            user = result.mappings().one_or_none()
            if not user:
                return list()
            phone = user["phone"]
            query_registrations = select(cls.model.__table__.columns).filter_by(phone=phone)
            result = await session.execute(query_registrations)
            return result.mappings().all()


class StaticsDAO(BaseDAO):
    model = StaticsDB

    @classmethod
    async def delete_all(cls):
        async with async_session_maker() as session:
            stmt = delete(cls.model)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get_order_list(cls, category: str, like: str):
        async with async_session_maker() as session:
            query = select(cls.model.__table__.columns).filter_by(category=category).\
                where(cls.model.title.like(f"%{like}%")).order_by(cls.model.title.asc())
            result = await session.execute(query)
            return result.mappings().all()
