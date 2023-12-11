import bcrypt
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .core.config import settings
from .admin.users.crud import create_user, get_user_by_name
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
        if not await get_user_by_name(session=session, name=default_user.name):
            await create_user(session=session, user_in=default_user)
