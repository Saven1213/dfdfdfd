from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton



main = InlineKeyboardMarkup(inline_keyboard=[
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
        InlineKeyboardButton(text='Мой конфиг', callback_data='my_profile')

    ],
    [
        InlineKeyboardButton(text='Служба поддержки', url='http://t.me/VPN548SupportBot')
    ]
])

profile_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Мои подарки', callback_data='gifts')
    ],
    [
        InlineKeyboardButton(text='Как использовать конфиг', callback_data='help_config')
    ],
    [
        InlineKeyboardButton(text='Рефералы', callback_data='referals')
    ],
    [
        InlineKeyboardButton(text='В главное меню', callback_data='to_main')
    ]
])



