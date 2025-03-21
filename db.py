import sqlite3
from datetime import datetime
from uuid import uuid4
import aiosqlite

# from aiogram.client.default import Default
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
#     username: Mapped[str] = mapped_column()
#     trial: Mapped[str] = mapped_column()
#     trial_end_date: Mapped[str] = mapped_column()
#     balance: Mapped[int] = mapped_column()
#     refferals: Mapped[int] = mapped_column()
#
# class Config(Base):
#     __tablename__ = 'configs'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     tg_id: Mapped[int] = mapped_column()
#     vpn_config: Mapped[str] = mapped_column()
#
#
# class Refferal(Base):
#     __tablename__ = 'refferals'
#     id: Mapped[int] = mapped_column(primary_key=True)
#     tg_id: Mapped[int] = mapped_column()
#     refferal: Mapped[int] = mapped_column()
#
#
# async def async_main():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
def check_user(tg_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users WHERE tg_id = ?
    """, (tg_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result
    else:
        return False

def add_user(tg_id, username):

    trial_start_date = datetime.now()
    trial_end_date_str = trial_start_date.strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (tg_id, trial, trial_end_date, balance, username, refferals) VALUES (?, ?, ?, ?, ?, ?)", (tg_id, 'True', trial_end_date_str, 0, username, 0))
    conn.commit()
    conn.close()

def set_trial_false(tg_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET trial = ? WHERE tg_id = ?", ('False', tg_id))
    conn.commit()
    conn.close()

def check_trial_():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT tg_id, trial_end_date FROM users WHERE trial = 'True'" )
    result = cursor.fetchall()
    conn.close()
    return result if result else None
    # async with aiosqlite.connect('database.db') as conn:
    #     cursor = await conn.execute("""
    #     SELECT trial, tg_id FROM users
    #     """)


def check_trial(tg_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT trial FROM users WHERE tg_id = ?", (tg_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 'False'

def get_trial_end_date(tg_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT trial_end_date FROM users WHERE tg_id = ?", (tg_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
    else:
        return None

def add_balance(tg_id, deposit):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT balance FROM users WHERE tg_id = ?
    """, (tg_id,))
    balance = cursor.fetchone()
    new_balance = balance[0] + deposit
    cursor.execute("""
    UPDATE users SET balance = ? WHERE tg_id = ?
    """, (new_balance, tg_id))
    conn.commit()
    conn.close()
    return True

def get_balance(tg_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT balance FROM users WHERE tg_id = ?
    """, (tg_id,))
    balance = cursor.fetchone()
    conn.close()
    if balance is not None:
        return balance[0]
    else:
        return 0

def get_configs(tg_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM configs WHERE tg_id = ?
    """, (tg_id,))
    configs = cursor.fetchall()
    conn.close()
    if len(configs) > 0:
        return configs
    else:
        return None

def check_refferals(tg_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT refferal FROM refferals WHERE tg_id = ?
    """, (tg_id,))
    amount = cursor.fetchall()
    conn.close()
    if amount:
        return amount
    else:
        return 'False'

def add_refferal(tg_id, username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO refferals (tg_id, refferal) VALUES (?, ?)
    """, (tg_id, username))
    conn.commit()
    conn.close()

def add_config(tg_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id FROM configs
    """)
    all_configs = cursor.fetchall()
    if len(all_configs) == 0:
        name = 'Конфиг N1'
    else:
        name_int = len(all_configs) + 1
        name = f'Конфиг N{str(name_int)}'

    test_config = str(uuid4())

    cursor.execute("""
    INSERT INTO configs (tg_id, vpn_config, name) VALUES (?, ?, ?)
    """, (tg_id, test_config, name))
    conn.commit()
    conn.close()
    return True

def check_config(tg_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM configs WHERE tg_id = ?
    """, (tg_id,))
    len_configs = cursor.fetchall()
    conn.close()
    return len_configs

# def update_config_(n_id):
#
#     conn = sqlite3.connect('database.db')
#     cursor = conn.cursor()
#
#     new_name = str(uuid4())
#
#     print(new_name, n_id)
#
#     cursor.execute("""
#     UPDATE configs SET vpn_config = ? WHERE id = ?
#     """, (new_name, n_id))
#     conn.commit()
#
#     conn.close()




async def update_config_(n_id):
    new_name = str(uuid4())

    async with aiosqlite.connect('database.db') as db:
        async with db.cursor() as cursor:
            await cursor.execute("""
            UPDATE configs SET vpn_config = ? WHERE id = ?
            """, (new_name, n_id))
            await db.commit()








