from aiogram import Bot
from aiogram.types import Message
from db import set_trial



async def end_trial(bot: Bot, message: Message):
    tg_id = message.from_user.id
    set_trial(tg_id)
    await bot.send_message(tg_id, "Ваша пробная подписка кончилась")