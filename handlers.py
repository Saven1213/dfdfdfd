import random
from gettext import textdomain
import aiosqlite


import base64
import asyncio
from idlelib.editor import keynames
from tabnanny import check

from aiogram import F, Router, Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery
from aiosend.loggers import invoice_polling
from typing_extensions import runtime

import Keyboards as kb
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiosend import CryptoPay

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import timedelta, datetime

from bot.db import check_user, add_user, check_trial, set_trial_false, get_trial_end_date, get_balance, get_configs, \
    add_balance, check_refferals, add_refferal, add_config, check_config, update_config_

router = Router()
bot = Bot

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')






@router.message(CommandStart())
async def startcmd(message: Message, command: CommandObject, bot: Bot):
    name = message.from_user.first_name
    tg_id = message.from_user.id
    user = check_user(tg_id)
    text = command.args
    username = message.from_user.username

    user_ref = check_user(text)


    if text is not None:
        if text != tg_id:
            if user:
                pass
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Профиль', callback_data='my_profile')
                    ],
                    [
                        InlineKeyboardButton(text='В главное меню', callback_data='to_main')
                    ]
                ])
                add_user(tg_id, username)
                await bot.send_message(chat_id=int(text), text='Вы привели нового человека, ваши деньги уже на балансе!', reply_markup=keyboard)
                user_refferals = check_refferals(text)
                user_lst = []
                for usr in user_refferals:
                    user_lst.append(usr[0])
                if user_lst[0] == 'False':
                    len_user = 'False'
                else:
                    len_user = len(user_lst)

                if len_user == 'False':


                    add_balance(text, 0.8)
                    add_refferal(text, username)
                    await message.answer(f'Вас пригласил @{user_ref[2]}!')

                elif len_user == 1:
                    add_balance(text, 1.6)
                    add_refferal(text, username)
                    await message.answer(f'Вас пригласил @{user_ref[2]}!')
                elif len_user == 2:
                    add_balance(text, 2)
                    add_refferal(text, username)
                    await message.answer(f'Вас пригласил @{user_ref[2]}!')
                elif len_user >= 3:
                    add_balance(text, 2.5)
                await message.answer(f'Вас пригласил @{user_ref[2]}!')

        else:
            await message.answer('Нельзя пригласить себя же!')
    else:
        add_user(tg_id, username)








    trial = check_trial(tg_id)
    balance = get_balance(tg_id)


    if trial == 'True' and balance == 0:
        await message.answer(f"""
        Добро пожаловать VPN548.

Спасибо, что присоединились к нам.

Хотим вам подарить 3 дня бесплатного сервиса, чтобы вы ощутили свободу!

Наш тариф 80₽/мес за 1 токен.

Подпишитесь на наш [канал](http://t.me/VPN548Me):)
        """, parse_mode='Markdown', reply_markup=kb.main)
    elif balance > 0:
        configs = get_configs(tg_id)
        if configs:
            amount_configs = check_config(tg_id)
            if len(amount_configs) < 2:

                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Справка', url='t.me/VPN548Bot/help')
                    ],
                    [
                        InlineKeyboardButton(text='Пополнить баланс', callback_data='deposit'),
                        InlineKeyboardButton(text='История платежей', callback_data='payment_history')
                    ],
                    [
                        InlineKeyboardButton(text='Как использовать конфиг?', callback_data='help_config')
                    ],
                    [
                        InlineKeyboardButton(text='Мой профиль', callback_data='my_profile'),
                        InlineKeyboardButton(text=f'Мои конфиги ({len(configs)})', callback_data='config_list')

                    ],

                    [
                        InlineKeyboardButton(text='Создать конфиг', callback_data='make_config')
                    ],

                    [
                        InlineKeyboardButton(text='Служба поддержки', url='http://t.me/VPN548SupportBot')
                    ]
                ])
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Справка', url='t.me/VPN548Bot/help')
                    ],
                    [
                        InlineKeyboardButton(text='Пополнить баланс', callback_data='deposit'),
                        InlineKeyboardButton(text='История платежей', callback_data='payment_history')
                    ],
                    [
                        InlineKeyboardButton(text='Как использовать конфиг?', callback_data='help_config')
                    ],
                    [
                        InlineKeyboardButton(text='Мой профиль', callback_data='my_profile'),
                        InlineKeyboardButton(text=f'Мои конфиги ({len(configs)})', callback_data='config_list')

                    ],



                    [
                        InlineKeyboardButton(text='Служба поддержки', url='http://t.me/VPN548SupportBot')
                    ]
                ])
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text='Справка', url='t.me/VPN548Bot/help')
                ],
                [
                    InlineKeyboardButton(text='Пополнить баланс', callback_data='deposit'),
                    InlineKeyboardButton(text='История платежей', callback_data='payment_history')
                ],
                [
                    InlineKeyboardButton(text='Как использовать конфиг?', callback_data='help_config')
                ],
                [
                    InlineKeyboardButton(text='Мой профиль', callback_data='my_profile'),
                    InlineKeyboardButton(text=f'Мои конфиги', callback_data='config_list')

                ],

                [
                    InlineKeyboardButton(text='Создать конфиг', callback_data='make_config')
                ],

                [
                    InlineKeyboardButton(text='Служба поддержки', url='http://t.me/VPN548SupportBot')
                ]
            ])


        await message.answer(f"""
                Добро пожаловать VPN548.

        Спасибо, что присоединились к нам.

        Хотим вам подарить 3 дня бесплатного сервиса, чтобы вы ощутили свободу!

        Наш тариф 80₽/мес за 1 токен.

        Подпишитесь на наш [канал](http://t.me/VPN548Me):)
                """, parse_mode='Markdown', reply_markup=keyboard)




    else:
        await message.answer(f"""
            Привет, {name}!👋

            Добро пожаловать в VPN548.

            К сожалению, деньги на вашем балансе закончились. Чтобы продолжить использовать наш VPN, пополните баланс 🌐

            Если вы не можете пополнить баланс прямо сейчас, нажмите на кнопку «Обещанный платеж», и сервис будет доступен до следующего дня.

            Напоминаем, наш тариф 80₽/мес за 1 токен.

            Подпишитесь на наш [канал](http://t.me/VPN548Me):)
                """, parse_mode='Markdown', reply_markup=kb.main)



@router.message(Command('help'))
async def helpcommand(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Справка VPN548', url='https://imgur.com/a/Wn1QAdZ')
        ],
        [
            InlineKeyboardButton(text='Служба Поддержки', url='http://t.me/VPN548SupportBot')
        ],
        [
            InlineKeyboardButton(text='В главное меню', callback_data='to_main')
        ]
    ])

    await message.answer('📖 Справка VPN548. Если вы не нашли ответ на свой вопрос, напишите в нашу 🛡 Службу поддержки',reply_markup=keyboard)



@router.callback_query(F.data == 'config_list')
async def configs_list(callback: CallbackQuery):
    tg_id = callback.from_user.id
    configs = get_configs(tg_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for item in configs:

        keyboard.inline_keyboard.append([
            InlineKeyboardButton(text=f"{item[3]}", callback_data=f'configs_{item[0]}_{item[3]}_{item[2]}')
        ])




    keyboard.inline_keyboard.append(
        [
            InlineKeyboardButton(text='В главное меню', callback_data='to_main')
        ]
    )
    await callback.message.edit_text("""
    Мои конфигурации

Выберете, про какую именно конфигурацию вы хотите узнать больше.
    """, reply_markup=keyboard)


@router.callback_query(F.data.split("_")[0] == 'configs')
async def config(callback: CallbackQuery):
    data = callback.data.split('_')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Удалить конфигурацию', callback_data='delete_config')
        ],
        [
            InlineKeyboardButton(text='Обновить конфигурацию', callback_data=f'update_config_{data[1]}')
        ],
        [
            InlineKeyboardButton(text='как использовать конфиг', callback_data='help_config')
        ],
        [
            InlineKeyboardButton(text='В главное меню', callback_data='to_main')
        ]
    ])
    print(data[1])

    await callback.message.edit_text(f"""
{data[2]}
 
<blockquote><code>{data[3]}</code></blockquote>
    
    """, parse_mode='HTML', reply_markup=keyboard)



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
    tg_id = callback.from_user.id
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
    tg_id = callback.from_user.id
    trial = check_trial(tg_id)
    balance = get_balance(tg_id)

    if trial == 'True' and balance == 0:
        await callback.message.edit_text(f"""
            Добро пожаловать VPN548.

    Спасибо, что присоединились к нам.

    Хотим вам подарить 3 дня бесплатного сервиса, чтобы вы ощутили свободу!

    Наш тариф 80₽/мес за 1 токен.

    Подпишитесь на наш [канал](http://t.me/VPN548Me):)
            """, parse_mode='Markdown', reply_markup=kb.main)
    elif balance > 0:
        configs = get_configs(tg_id)
        if configs:
            amount_configs = check_config(tg_id)
            if len(amount_configs) < 2:

                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Справка', url='t.me/VPN548Bot/help')
                    ],
                    [
                        InlineKeyboardButton(text='Пополнить баланс', callback_data='deposit'),
                        InlineKeyboardButton(text='История платежей', callback_data='payment_history')
                    ],
                    [
                        InlineKeyboardButton(text='Как использовать конфиг?', callback_data='help_config')
                    ],
                    [
                        InlineKeyboardButton(text='Мой профиль', callback_data='my_profile'),
                        InlineKeyboardButton(text=f'Мои конфиги ({len(configs)})', callback_data='config_list')

                    ],

                    [
                        InlineKeyboardButton(text='Создать конфиг', callback_data='make_config')
                    ],

                    [
                        InlineKeyboardButton(text='Служба поддержки', url='http://t.me/VPN548SupportBot')
                    ]
                ])
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text='Справка', url='t.me/VPN548Bot/help')
                    ],
                    [
                        InlineKeyboardButton(text='Пополнить баланс', callback_data='deposit'),
                        InlineKeyboardButton(text='История платежей', callback_data='payment_history')
                    ],
                    [
                        InlineKeyboardButton(text='Как использовать конфиг?', callback_data='help_config')
                    ],
                    [
                        InlineKeyboardButton(text='Мой профиль', callback_data='my_profile'),
                        InlineKeyboardButton(text=f'Мои конфиги ({len(configs)})', callback_data='config_list')

                    ],

                    [
                        InlineKeyboardButton(text='Служба поддержки', url='http://t.me/VPN548SupportBot')
                    ]
                ])
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text='Справка', url='t.me/VPN548Bot/help')
                ],
                [
                    InlineKeyboardButton(text='Пополнить баланс', callback_data='deposit'),
                    InlineKeyboardButton(text='История платежей', callback_data='payment_history')
                ],
                [
                    InlineKeyboardButton(text='Как использовать конфиг?', callback_data='help_config')
                ],
                [
                    InlineKeyboardButton(text='Мой профиль', callback_data='my_profile'),
                    InlineKeyboardButton(text=f'Мои конфиги', callback_data='config_list')

                ],

                [
                    InlineKeyboardButton(text='Создать конфиг', callback_data='make_config')
                ],

                [
                    InlineKeyboardButton(text='Служба поддержки', url='http://t.me/VPN548SupportBot')
                ]
            ])

        await callback.message.edit_text(f"""
                    Добро пожаловать VPN548.

            Спасибо, что присоединились к нам.

            Хотим вам подарить 3 дня бесплатного сервиса, чтобы вы ощутили свободу!

            Наш тариф 80₽/мес за 1 токен.

            Подпишитесь на наш [канал](http://t.me/VPN548Me):)
                    """, parse_mode='Markdown', reply_markup=keyboard)




    else:
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
            InlineKeyboardButton(text='Отправить', switch_inline_query='')
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

    await callback.message.edit_text(f"""
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
https://t.me/MyFirstTrainingEasy_bot?start={callback.from_user.id}
    """, reply_markup=keyboard)

@router.callback_query(F.data == 'prof_balance')
async def balance_wind(callback: CallbackQuery):
    tg_id = callback.from_user.id
    balance = get_balance(tg_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Назад', callback_data='my_profile')
        ]
    ])

    await callback.message.edit_text(f"""
Твой баланс:

<blockquote><code>{balance} USDT</code></blockquote> 
    """, parse_mode='HTML', reply_markup=keyboard)


# @router.message(Command('prize_secret'))
# async def get_gift(message: Message, command: CommandObject):


@router.callback_query(F.data == 'make_config')
async def make_config(callback: CallbackQuery):
    tg_id = callback.from_user.id
    add_config(tg_id)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Мои конфиги', callback_data='config_list')
        ],
        [
            InlineKeyboardButton(text='В главное меню', callback_data='to_main')
        ]
    ])

    await callback.message.edit_text('Конфиг создан!', reply_markup=keyboard)

@router.callback_query(F.data.startswitch('update_config'))
async def update_config(callback: CallbackQuery):
    data = callback.data.split('_')[1]
    n_id = int(data)
    await update_config_(n_id)

    async with aiosqlite.connect('database.db') as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT name, description, vpn_config FROM configs WHERE id = ?", (n_id,))
            updated_config = await cursor.fetchone()

            if updated_config:
                name, description, vpn_config = updated_config
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text='В главное меню', callback_data='to_main')
                    ]
                ])

                await callback.message.edit_text(f"""
                {description}
            
                <blockquote><code>{vpn_config}</code></blockquote>
                        """, parse_mode='HTML', reply_markup=keyboard)
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text='В главное меню', callback_data='to_main')
                    ]
                ])

                await callback.message.edit_text("Конфигурация не найдена",
                                                 reply_markup=keyboard)  # Обработка случая, когда конфигурация не найдена



