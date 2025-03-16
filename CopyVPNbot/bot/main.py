from aiogram import Bot, Dispatcher
import asyncio
from Config import KEY
import logging



# from bot.db import async_main
from handlers import router
from Config import PAYTOKEN
from aiosend import CryptoPay


cp = CryptoPay(PAYTOKEN)


async def main():
    bot = Bot(token=KEY)
    await bot.delete_webhook(drop_pending_updates=True)
    # await async_main()
    dp = Dispatcher()
    dp.include_router(router)
    try:

        await asyncio.gather(
            dp.start_polling(bot, cp=cp),
            cp.start_polling(),
        )
    except:
        await dp.stop_polling()
        await bot.session.close()



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())