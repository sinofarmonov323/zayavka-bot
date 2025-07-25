from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import logging, asyncio
from keyboards import send_buttons
from database import add_user

dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    add_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Salom {message.from_user.full_name}")

@dp.chat_join_request()
async def handle_chat_join_request(event: types.ChatJoinRequest, bot: Bot):   
    add_user(event.from_user.id, event.from_user.username) 
    await bot.send_photo(event.from_user.id, photo=types.FSInputFile("image.png"), caption="𝗔𝘀𝘀𝗮𝗹𝗼𝗺𝘂 𝗮𝗹𝗮𝘆𝗸𝘂𝗺😊\n\n𝗦𝗶𝘇 𝗩𝗶𝗽 𝗸𝗮𝗻𝗮𝗹 𝘃𝗮 𝗦𝗵𝗼𝗸𝗵 𝗮𝗸𝗲𝗻𝗶𝗻𝗴 𝟯𝟬𝟬𝟬$ 𝗹𝗶𝗸 𝗸𝘂𝗿𝘀𝗶𝗻𝗶 𝘆𝘂𝘁𝗶𝗯 𝗼𝗹𝗱𝗶𝗻𝗴𝗶𝘇😎\n\n𝗨𝗹𝗮𝗿𝗻𝗶 𝗾𝗼𝗹𝗴𝗮 𝗸𝗶𝗿𝗶𝘁𝗶𝘀𝗵 𝘂𝗰𝗵𝘂𝗻 𝗽𝗮𝘀𝗱𝗮𝗴𝗶 𝗧𝘂𝗴𝗺𝗮𝗹𝗮𝗿𝗱𝗮𝗻 𝗳𝗼𝘆𝗱𝗮𝗹𝗮𝗻𝗶𝗻𝗴👇", reply_markup=(send_buttons("https://t.me/+ZeVl1BrIZWo0NmEy", "https://t.me/+ki3LHeP7FStlMmUy")))
    # await event.approve() # bu kod foydalanuvchi zayavka tashalasa avtomatik qabul qiladi1

@dp.message()
async def handle(message: types.Message):
    print(f"{message.from_user.username} - {message.text}\n{message}")

async def main():
    bot = Bot("8374612411:AAGcRoyFwjTIPUVC3cyzYEEk0WUZrQErlPg")
    await dp.start_polling(bot)


if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
