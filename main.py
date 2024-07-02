# ---------------------------------------------------
# modules
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command

# ---------------------------------------------------
# constants
BOT_TOKEN = input("input bot token: ")
if BOT_TOKEN == "":
    raise ValueError("bot token cannot be empty")

# ---------------------------------------------------
# code
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(text="hello, {}".format(message.from_user.full_name))

@dp.message(Command("help"))
async def handle_help(message: types.Message):
    await message.answer(text="send any message to echo it back")

@dp.message()
async def echo_message(message: types.Message):
    #await bot.send_message(
    #    chat_id=message.chat_id,
    #    text="placeholder"
    #)
    await message.answer(text=message.text)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())