from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from sqlalchemy.orm import Session
from data.models import User

async def add_user(user_id: int, username: str, role: str, session: AsyncSession):
    """
    Функция для добавления пользователя в базу данных.
    """
    # Проверяем, существует ли уже пользователь в базе данных
    result = await session.execute(select(User).where(User.telegram_id == user_id))
    user = result.scalars().first()

    if user:
        # Если пользователь уже существует, обновляем его роль
        user.role = role
        await session.commit()
    else:
        # Если пользователя нет в базе, создаем нового
        new_user = User(
            telegram_id=user_id,
            username=username,
            role=role
        )
        session.add(new_user)
        await session.commit()

# Функция для получения всех пользователей
async def get_all_users(session: AsyncSession) -> List[User]:
    result = await session.execute(select(User))  # Получаем всех пользователей
    users = result.scalars().all()  # Возвращаем список пользователей
    return users

# Функция для обновления профиля пользователя
async def update_user_profile(user_id: int, field_name: str, new_value: str, session: AsyncSession) -> bool:
    try:
        # Найдем пользователя по telegram_id
        stmt = select(User).filter(User.telegram_id == user_id)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if user:
            # Обновим соответствующее поле
            setattr(user, field_name, new_value)

            # Добавляем пользователя обратно в сессию и сохраняем изменения
            session.add(user)
            await session.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Ошибка при обновлении профиля: {e}")
        return False

async def update_visibility(user_id: int, value: bool, session: AsyncSession):
    result = await session.execute(
        select(User).filter(User.telegram_id == user_id)
    )
    user = result.scalars().first()
    if user:
        user.visibility = value
        session.add(user)
        await session.commit()

async def get_user(session: Session, telegram_id: int):
    stmt = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_users_by_direction_and_visibility(direction: str, session: AsyncSession):
    result = await session.execute(
        select(User).filter(User.direction == direction, User.visibility == True)
    )
    return result.scalars().all()