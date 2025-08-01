from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def send_buttons(url1: str, url2: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 VIP Kanalga kirish", url=url1)],
        [InlineKeyboardButton(text="🎁 Kursni olish", url=url2)]
    ])

def admin_panel_buttons():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Xabar yuborish")],
            [KeyboardButton(text="Zakazlar tarixini ko'rish")]
        ]
    )
