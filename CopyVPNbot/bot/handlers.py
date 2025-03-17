import random
from gettext import textdomain


from aiogram import F, Router, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiosend.loggers import invoice_polling
from typing_extensions import runtime

import Keyboards as kb
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiosend import CryptoPay

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timedelta, datetime

from bot.db import check_user, add_user, check_trial
from bot.scheduler import end_trial



router = Router()
bot = Bot


scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
scheduler.add_job(end_trial, 'date', run_date=datetime.now() + timedelta(days=3),
                  kwargs={'bot': bot})
scheduler.start()



@router.message(CommandStart())
async def startcmd(message: Message):
    name = message.from_user.first_name
    tg_id = message.from_user.id
    user = check_user(tg_id)
    if user:
        pass
    else:
        add_user(tg_id)

    trial = check_trial(tg_id)



    if trial == 'True':
        await message.answer(f"""
        Добро пожаловать VPN548.

Спасибо, что присоединились к нам.

Хотим вам подарить 3 дня бесплатного сервиса, чтобы вы ощутили свободу!

Наш тариф 80₽/мес за 1 токен.

Подпишитесь на наш [канал](http://t.me/VPN548Me):)
        """, parse_mode='Markdown', reply_markup=kb.main)
    else:
        await message.answer(f"""
            Привет, {name}!👋

            Добро пожаловать в VPN548.

            К сожалению, деньги на вашем балансе закончились. Чтобы продолжить использовать наш VPN, пополните баланс 🌐

            Если вы не можете пополнить баланс прямо сейчас, нажмите на кнопку «Обещанный платеж», и сервис будет доступен до следующего дня.

            Напоминаем, наш тариф 80₽/мес за 1 токен.

            Подпишитесь на наш [канал](http://t.me/VPN548Me):)
                """, parse_mode='Markdown', reply_markup=kb.main)

@router.callback_query(F.data == "deposit")
async def deposit(callback: CallbackQuery, cp: CryptoPay):
    sum1 = '0.8'
    sum2 = '1.6'
    sum3 = '3.2'
    sum4 = '4'
    sum5 = '8'
    sum6 = '16'





    keyboard = InlineKeyboardMarkup(inline_keyboard=[

        [
            # InlineKeyboardButton(text='0.8 usdt.', callback_data=f'sum-{sum1}'),
            InlineKeyboardButton(text='0.8 usdt.', callback_data=f'sum-{sum1}'),
            InlineKeyboardButton(text='1.6 usdt.', callback_data=f'sum-{sum2}'),
            InlineKeyboardButton(text='3.2 usdt.', callback_data=f'sum-{sum3}')
        ],
        [
            InlineKeyboardButton(text='4 usdt.', callback_data=f'sum-{sum4}'),
            InlineKeyboardButton(text='8 usdt.', callback_data=f'sum-{sum5}')
        ],
        [
            InlineKeyboardButton(text='16 usdt.', callback_data=f'sum-{sum6}')
        ],
        [
            InlineKeyboardButton(text='Ввести свою сумму', callback_data='sum7c')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='to_main')
        ]
    ])

    await callback.message.edit_text('''Выберете сумму пополнения

Напомню, наш тариф: 1 конфиг - 0.8 usdt/мес.''', reply_markup=keyboard)

@router.callback_query(F.data.split("-")[0] == 'sum')
async def get_invoice(callback: CallbackQuery, cp: CryptoPay):
    data = callback.data.split('-')[1]
    invoice = await cp.create_invoice(float(data), "USDT")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Оплатить CryptoBot', url=invoice.mini_app_invoice_url)
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='back1')
        ]
    ])


    await callback.message.edit_text('Выберите действие: ', reply_markup=keyboard)






#     await callback.message.edit_text(f"""
# Счет №{invoice_number}.
#
# У вас есть 10 минут для оплаты. После этого счёт будет отменен.
#     """)
#
# async def generate_numeric_invoice_number(length=16):
#     """Генерирует случайный номер счета, состоящий только из цифр."""
#     return ''.join(random.choices('0123456789', k=length))

class Amount(StatesGroup):
    amount = State()

@router.callback_query(F.data == 'sum7c')
async def sumc_deposit(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Amount.amount)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='back1')
        ]
    ])
    await callback.message.edit_text("""
    Введите сумму, на которую хотите пополнить баланс:\n
    Сумма должна быть от 80 руб.
    """, reply_markup=keyboard)

@router.callback_query(F.data == 'back1')
async def back1(callback: CallbackQuery, state: FSMContext):
    sum1 = '0.8'
    sum2 = '1.6'
    sum3 = '3.2'
    sum4 = '4'
    sum5 = '8'
    sum6 = '16'

    keyboard = InlineKeyboardMarkup(inline_keyboard=[

        [
            InlineKeyboardButton(text='0.8 usdt.', callback_data=f'sum-{sum1}'),
            InlineKeyboardButton(text='1.6 usdt.', callback_data=f'sum-{sum2}'),
            InlineKeyboardButton(text='3.2 usdt.', callback_data=f'sum-{sum3}')
        ],
        [
            InlineKeyboardButton(text='4 usdt.', callback_data=f'sum-{sum4}'),
            InlineKeyboardButton(text='8 usdt.', callback_data=f'sum-{sum5}')
        ],
        [
            InlineKeyboardButton(text='16 usdt.', callback_data=f'sum-{sum6}')
        ],
        [
            InlineKeyboardButton(text='Ввести свою сумму', callback_data='sum7c')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='to_main')
        ]
    ])
    await state.clear()
    await callback.message.edit_text("""
    Введите сумму, на которую хотите пополнить баланс:\n
    Сумма должна быть от 80 руб.
    """, reply_markup=keyboard)

@router.message(Amount.amount)
async def enter_amount(message: Message, state: FSMContext, cp: CryptoPay):

    data = message.text

    try:
        new_data = float(data)
        if type(new_data) == float:
            invoice = await cp.create_invoice(float(data), 'USDT')
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text='Оплатить CryptoBot', url=invoice.mini_app_invoice_url)
                ],
                [
                    InlineKeyboardButton(text='Назад', callback_data='back1')
                ]
            ])
            await message.answer('Выберите действие: ', reply_markup=keyboard)
        else:
            pass
    except ValueError:
        await message.answer('Введите число USDT')


    # try:
    #     if type(float(data)) == float:
    #         invoice = cp.create_invoice(float(data), 'USDT')
    #         keyboard = InlineKeyboardMarkup(inline_keyboard=[
    #             [
    #                 InlineKeyboardButton(text='Оплатить CryptoBot', url=invoice.mini_app_invoice_url)
    #             ]
    #         ])
    #
    #         await message.edit_text('Выберите действие: ', reply_markup=keyboard)
    #     else:
    #         pass
    # except:
    #     await message.answer('Введите число USDT')



@router.callback_query(F.data == 'to_main')
async def main_page(callback: CallbackQuery):
    name = callback.from_user.first_name
    await callback.message.edit_text(f"""
        Привет, {name}!👋

    Добро пожаловать в VPN548.

    К сожалению, деньги на вашем балансе закончились. Чтобы продолжить использовать наш VPN, пополните баланс 🌐

    Если вы не можете пополнить баланс прямо сейчас, нажмите на кнопку «Обещанный платеж», и сервис будет доступен до следующего дня.

    Напоминаем, наш тариф 80₽/мес за 1 токен.

    Подпишитесь на наш [канал](http://t.me/VPN548Me):)
        """, parse_mode='Markdown', reply_markup=kb.main)

@router.callback_query(F.data == 'help_config')
async def help_config(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='to_main')
        ]
    ])

    await callback.message.edit_text("""
    1. Скачайте и установите на устройство приложение Outline:


[Приложение для iOS](https://itunes.apple.com/app/outline-app/id1356177741)
[Приложение для macOS](https://itunes.apple.com/app/outline-app/id1356178125)
[Приложение для Windows](https://s3.amazonaws.com/outline-releases/client/windows/stable/Outline-Client.exe)
[Приложение для Linux](https://s3.amazonaws.com/outline-releases/client/linux/stable/Outline-Client.AppImage)
[Приложение для Android](https://play.google.com/store/apps/details?id=org.outline.android.client)
[Доп приложение для Android](https://s3.amazonaws.com/outline-releases/client/android/stable/Outline-Client.apk)

2. Получите ключ доступа, который начинается с ss://, а затем скопируйте его.

3. Откройте клиент Outline. Если ваш ключ доступа определился автоматически, нажмите "Подключиться". Если этого не произошло, вставьте ключ в поле и нажмите "Подключиться".

Теперь у вас есть доступ к свободному интернету. Чтобы убедиться, что вы подключились к серверу, введите в Google Поиске фразу "Какой у меня IP-адрес". IP-адрес, указанный в Google, должен совпадать с IP-адресом в клиенте Outline.
    """, parse_mode='Markdown', reply_markup=keyboard)

@router.callback_query(F.data == 'my_profile')
async def profile(callback: CallbackQuery):
    tg_id = callback.from_user.id
    await callback.message.edit_text(f"""
    Мой профиль\n
    Мой Telegram ID: {tg_id} 
    """, reply_markup=kb.profile_keyboard)

@router.callback_query(F.data == 'gifts')
async def gifts(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Отправить', callback_data='send_gift')
        ],
        [
            InlineKeyboardButton(text='Назад', callback_data='my_profile')
        ]
    ])

    await callback.message.edit_text('Мои подарки', reply_markup=keyboard)



@router.callback_query(F.data == 'referals')
async def referals(callback: CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='my_profile')
        ]
    ])

    await callback.message.edit_text("""
    💰 Приглашайте активных пользователей в бот и получайте вознаграждения!\n
\n
Вы получаете следующие вознаграждения за приглашённых пользователей:\n
\n
• При приведении первого друга вам будет зачислена сумма на баланс, эквивалентная 5 дням.\n
\n
• При приведении второго друга — 3 дня.\n
\n
• При приведении третьего друга — 1 день.\n
\n
Скопируйте ссылку ниже, чтобы пригласить рефералов:
t.me/VPN548Bot?start=r-873034839
    """, reply_markup=keyboard)


