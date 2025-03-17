from datetime import datetime

from aiogram import Bot, Dispatcher
import asyncio
from Config import KEY
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from handlers import router
from Config import PAYTOKEN
from aiosend import CryptoPay
# from db import async_main

cp = CryptoPay(PAYTOKEN)
bot = Bot(token=KEY)

async def main():

    await bot.delete_webhook(drop_pending_updates=True)
    # await async_main()
    dp = Dispatcher()
    dp.include_router(router)

    # await async_main()
    try:

        await asyncio.gather(
            dp.start_polling(bot, cp=cp),
            cp.start_polling(),
        )
    except:
        print('БОТ выключен!')
        await dp.stop_polling()
        await bot.session.close()

@cp.invoice_polling()
async def handle_payment(invoice, message):
    await message.answer(f"invoice #{invoice.invoice_id} has been paid")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
