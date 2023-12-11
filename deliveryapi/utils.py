from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from .core.config import settings
from .admin.users.crud import create_user
from .admin.users.schemas import UserCreate


async def startup():
    engine = create_async_engine(settings.db.url)
    async_session = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    default_user = UserCreate(name=settings.superuser.name, password=settings.superuser.password)

    async with async_session() as session:
        await create_user(session=session, user_in=default_user)
