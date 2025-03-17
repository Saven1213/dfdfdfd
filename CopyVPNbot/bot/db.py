import sqlite3
from aiogram import Bot
from aiogram.types import Message
# from sqlalchemy import String, ForeignKey
# from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column
# from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, async_session
#
#
# engine = create_async_engine(url='sqlite+aiosqlite:///database.db')
#
# async_sess = async_sessionmaker(engine)
#
# class Base(AsyncAttrs, DeclarativeBase):
#     pass
#
# class User(Base):
#     __tablename__ = 'users'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     tg_id: Mapped[int] = mapped_column()
#     trial: Mapped[str] = mapped_column()
#
#
# async def async_main():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


def check_user(tg_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users WHERE tg_id = ?
    """, (tg_id,))
    result = cursor.fetchone()
    conn.close()
    if result is not None:
        return True
    else:
        return False

def add_user(tg_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO users (tg_id, trial) VALUES (?,?)
    """, (tg_id, 'True'))
    conn.commit()
    conn.close()

def check_trial(tg_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT trial FROM users WHERE tg_id = ?
    """, (tg_id,))
    res = cursor.fetchone()
    conn.close()
    return res[0]

def set_trial(tg_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE users SET trial = 'False' WHERE tg_id = ?
    """, (tg_id,))
    conn.commit()
    conn.close()

