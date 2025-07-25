from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def send_buttons(url1: str, url2: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 VIP Kanalga kirish", url=url1)],
        [InlineKeyboardButton(text="🎁 Kursni olish", url=url2)]
    ])
