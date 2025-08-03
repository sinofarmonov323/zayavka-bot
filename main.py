from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command, CommandObject, and_f, StateFilter
import logging, asyncio
from keyboards import send_buttons, admin_panel_buttons
from database import add_user, get_users
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

dp = Dispatcher()

ADMIN_ID = 5020353042

class AdminStates(StatesGroup):
    send_message = State()

@dp.message(CommandStart())
async def start(message: types.Message):
    add_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Salom {message.from_user.full_name}")

@dp.chat_join_request()
async def handle_chat_join_request(event: types.ChatJoinRequest, bot: Bot):   
    add_user(event.from_user.id, event.from_user.username) 
    await bot.send_photo(event.from_user.id, photo=types.FSInputFile("image.png"), caption="𝗔𝘀𝘀𝗮𝗹𝗼𝗺𝘂 𝗮𝗹𝗮𝘆𝗸𝘂𝗺😊\n\n𝗦𝗶𝘇 𝗩𝗶𝗽 𝗸𝗮𝗻𝗮𝗹 𝘃𝗮 𝗦𝗵𝗼𝗸𝗵 𝗮𝗸𝗲𝗻𝗶𝗻𝗴 𝟯𝟬𝟬𝟬$ 𝗹𝗶𝗸 𝗸𝘂𝗿𝘀𝗶𝗻𝗶 𝘆𝘂𝘁𝗶𝗯 𝗼𝗹𝗱𝗶𝗻𝗴𝗶𝘇😎\n\n𝗨𝗹𝗮𝗿𝗻𝗶 𝗾𝗼𝗹𝗴𝗮 𝗸𝗶𝗿𝗶𝘁𝗶𝘀𝗵 𝘂𝗰𝗵𝘂𝗻 𝗽𝗮𝘀𝗱𝗮𝗴𝗶 𝗧𝘂𝗴𝗺𝗮𝗹𝗮𝗿𝗱𝗮𝗻 𝗳𝗼𝘆𝗱𝗮𝗹𝗮𝗻𝗶𝗻𝗴👇", reply_markup=(send_buttons("https://t.me/+ZeVl1BrIZWo0NmEy", "https://t.me/+ki3LHeP7FStlMmUy")))
    # await event.approve() # bu kod foydalanuvchi zayavka tashalasa avtomatik qabul qiladi1

@dp.message(and_f(F.chat.id == ADMIN_ID, F.text.startswith("/admin")))
async def admin_command_handler(message: types.Message):
    await message.answer("Admin panel", reply_markup=admin_panel_buttons())

@dp.message(and_f(F.chat.id == ADMIN_ID, F.text.in_(["Xabar yuborish", "Zakazlar tarixini ko'rish"])))
async def admin_message_handler(message: types.Message, state: FSMContext):
    if message.text == "Xabar yuborish":
        await message.answer("Xabaringizni yuboring")
        await state.set_state(AdminStates.send_message)
    elif message.text == "Statistika":
        await message.answer("statistika")

@dp.message(StateFilter(AdminStates.send_message))
async def send_message_handler(message: types.Message, state: FSMContext, bot: Bot):
    if message.content_type == "photo":
        for user in get_users():
            await bot.send_photo(user['user_id'], message.photo[-1].file_id, caption=message.caption)
    elif message.content_type == "video":
        for user in get_users():
            await bot.send_video(user['user_id'], message.video.file_id, caption=message.caption)
    else:
        for user in get_users():
            await bot.send_message(user['user_id'], message.text)
    
    await message.answer("Xabar yuborildi")
    await state.clear()

@dp.message(Command("m"))
async def send_message_to_users(message: types.Message, bot: Bot, command: CommandObject):
    args = command.args
    if args != None:
        for user in get_users():
            await bot.send_message(user['user_id'], args)
    else:
        await message.answer("ishlatish: /m [xabar]")

@dp.message()
async def handle(message: types.Message):
    print(f"{message.from_user.username} - {message.text}\n{message}")

async def main():
    bot = Bot("token")
    await dp.start_polling(bot)


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
