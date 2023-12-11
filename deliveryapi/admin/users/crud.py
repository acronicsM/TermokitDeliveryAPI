from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from deliveryapi.core.models import User
from .schemas import UserCreate


async def get_user(user_id: int, session: AsyncSession) -> User | None:
    return await session.get(User, user_id)


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    users = list(users)
    return users


async def active_user(user: User, session: AsyncSession, is_active: bool) -> User:
    if user.is_active != is_active:
        user.is_active = is_active
        await session.commit()
    return user


async def del_user(session: AsyncSession, user: User) -> None:
    await session.delete(user)
    await session.commit()


async def create_user(session: AsyncSession, user_in: UserCreate) -> User:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()

    return user
