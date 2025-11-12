from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, and_f, StateFilter
import logging, asyncio
from keyboards import send_buttons, admin_panel_buttons
from database import add_user, get_users, add_text, get_text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

dp = Dispatcher()

ADMINS_ID = [7972249893, 7077167971]

class AdminStates(StatesGroup):
    send_message = State()

class ReceiveText(StatesGroup):
    waiting_for_text = State()

class ReceiveChannels(StatesGroup):
    wait_for_urls = State()
    wait_for_texts = State()

class SendMessageToEveryUser(StatesGroup):
    wait_for_message = State()

@dp.message(CommandStart())
async def start(message: types.Message):
    add_user(message.from_user.id, message.from_user.username)
    data = get_text()[0]
    try:
        if "\n\n\n" in data['text']:
            text = data['text'].split("\n\n\n")[0]
            urls = data['text'].split("\n\n\n")[1].split("\n")
        else:
            text = data['text']
            urls = []
        if data['image'] == "none":
            await message.answer(text, reply_markup=send_buttons(urls) if urls else None)
        else:
            await message.answer_photo(photo=data['image'], caption=text, reply_markup=send_buttons(urls) if urls else None)
    except Exception as e:
        print(e)

@dp.chat_join_request()
async def handle_chat_join_request(event: types.ChatJoinRequest, bot: Bot):
    add_user(event.from_user.id, event.from_user.username)
    data = get_text()[0]
    try:
        if "\n\n\n" in data['text']:
            text = data['text'].split("\n\n\n")[0]
            urls = data['text'].split("\n\n\n")[1].split("\n")
        else:
            text = data['text']
            urls = []
        if data['image'] == "none":
            await bot.send_message(event.from_user.id, text, reply_markup=send_buttons(urls) if urls else None)
        else:
            await bot.send_photo(event.from_user.id, photo=data['image'], caption=text, reply_markup=send_buttons(urls) if urls else None)
    except Exception as e:
        print(e)

@dp.message(and_f(F.chat.id.in_(ADMINS_ID), F.text.startswith("/admin")))
async def admin_command_handler(message: types.Message):
    await message.answer("Admin panel", reply_markup=admin_panel_buttons())

@dp.message(and_f(F.chat.id.in_(ADMINS_ID), F.text.in_(["Matnni o'zgartirish", "Statistika", "Foydalanuvchilarga xabar yuborish"])))
async def admin_message_handler(message: types.Message, state: FSMContext):
    if message.text == "Statistika":
        await message.answer("Foydalanuvchilar soni: " + str(len(get_users())))
    elif message.text == "Matnni o'zgartirish":
        await message.answer("Yangi matnni yuboring")
        await state.set_state(ReceiveText.waiting_for_text)
    elif message.text == "Foydalanuvchilarga xabar yuborish":
        await message.answer("Yuboriladigan xabarni yuboring")
        await state.set_state(SendMessageToEveryUser.wait_for_message)

@dp.message(StateFilter(SendMessageToEveryUser.wait_for_message))
async def send_message_to_all_handler(message: types.Message, state: FSMContext, bot: Bot):
    global urls, text
    urls = []
    text = ""
    try:
        if message.content_type == "text":
            if "\n\n\n" in message.text:
                text = message.text.split("\n\n\n")[0]
                urls = message.text.split("\n\n\n")[1].split("\n")
            else:
                text = message.text
            for user in get_users():
                await bot.send_message(user['user_id'], text, reply_markup=send_buttons(urls) if urls else None)
            await message.answer("Xabar foydalanuvchilarga yuborildi")
            await state.clear()
        elif message.content_type == "photo":
            if "\n\n\n" in message.caption:
                text = message.caption.split("\n\n\n")[0]
                urls = message.caption.split("\n\n\n")[1].split("\n")
            else:
                text = message.caption
            for user in get_users():
                await bot.send_photo(user['user_id'], photo=message.photo[-1].file_id, caption=text, reply_markup=send_buttons(urls) if urls else None)
            await message.answer("Xabar foydalanuvchilarga yuborildi")
            await state.clear()
        elif message.content_type == "video":
            if "\n\n\n" in message.caption:
                text = message.caption.split("\n\n\n")[0]
                urls = message.caption.split("\n\n\n")[1].split("\n")
            else:
                text = message.caption
            for user in get_users():
                await bot.send_video(user['user_id'], video=message.video.file_id, caption=text, reply_markup=send_buttons(urls) if urls else None)
            await message.answer("Xabar foydalanuvchilarga yuborildi")
            await state.clear()
        else:
            await message.answer("Faqat matn yoki rasm yuboring")
    except Exception as e:
        print(e)
        await state.clear()

@dp.message(StateFilter(ReceiveText.waiting_for_text))
async def receive_text_handler(message: types.Message, state: FSMContext):
    if message.content_type == "text":
        await message.answer("Matn o'zgartirildi")
        add_text(message.text, "none")
        await state.clear()
    elif message.content_type == "photo":
        await message.answer("Matn o'zgartirildi")
        add_text(message.caption, message.photo[-1].file_id)
        await state.clear()
    else:
        await message.answer("Faqat matn yuboring")

@dp.message()
async def handle(message: types.Message):
    print(f"{message.from_user.username} - {message.text}\n{message}")

async def main():
    bot = Bot("7969330020:AAFF7UA0J56xv_-Z2Ge-SPHmPLH9pkVIdb0") # 7969330020:AAFF7UA0J56xv_-Z2Ge-SPHmPLH9pkVIdb0
    await dp.start_polling(bot)


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
