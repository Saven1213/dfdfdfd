import random
from gettext import textdomain

from aiogram import F, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
import Keyboards as kb
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiosend import CryptoPay

router = Router()


@router.message(CommandStart())
async def startcmd(message: Message):
    name = message.from_user.first_name
    await message.answer(f"""
    Привет, {name}!👋

Добро пожаловать в VPN548.

К сожалению, деньги на вашем балансе закончились. Чтобы продолжить использовать наш VPN, пополните баланс 🌐

Если вы не можете пополнить баланс прямо сейчас, нажмите на кнопку «Обещанный платеж», и сервис будет доступен до следующего дня.

Напоминаем, наш тариф 80₽/мес за 1 токен.

Подпишитесь на наш [канал](http://t.me/VPN548Me):)
    """, parse_mode='Markdown', reply_markup=kb.main)

@router.callback_query(F.data == "deposit")
async def deposit(callback: CallbackQuery):
    sum1 = '8'
    sum2 = '160'
    sum3 = '320'
    sum4 = '400'
    sum5 = '800'
    sum6 = '1600'


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

    await callback.message.edit_text('''Выберете сумму пополнения

Напомню, наш тариф: 1 конфиг - 0.8 usdt/мес.''', reply_markup=keyboard)

@router.callback_query(F.data.startswitch('sum'))
async def get_invoice(message, callback: CallbackQuery, cp:CryptoPay):
    data = callback.data.split('-')[1]
    invoice = await cp.create_invoice(int(data), "USDT")
    await message.answer(f"pay: {invoice.bot_invoice_url}")






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
    sum1 = '80'
    sum2 = '160'
    sum3 = '320'
    sum4 = '400'
    sum5 = '800'
    sum6 = '1600'

    keyboard = InlineKeyboardMarkup(inline_keyboard=[

        [
            InlineKeyboardButton(text='80 руб.', callback_data=f'sum-{sum1}'),
            InlineKeyboardButton(text='160 руб.', callback_data=f'sum-{sum2}'),
            InlineKeyboardButton(text='320 руб.', callback_data=f'sum-{sum3}')
        ],
        [
            InlineKeyboardButton(text='400 руб.', callback_data=f'sum-{sum4}'),
            InlineKeyboardButton(text='800 руб.', callback_data=f'sum-{sum5}')
        ],
        [
            InlineKeyboardButton(text='1600 руб.', callback_data=f'sum-{sum6}')
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


