from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def send_buttons(urls):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=" ".join(url.split(" ")[1:]), url=url.split(" ")[0])] for url in urls
    ])

def admin_panel_buttons():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Statistika")],
            [KeyboardButton(text="Matnni o'zgartirish"), KeyboardButton(text="Foydalanuvchilarga xabar yuborish")],
        ]
    )
