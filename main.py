# ---------------------------------------------------
# modules
import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandObject, CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode

# ---------------------------------------------------
# constants
BOT_TOKEN = input("input bot token: ")
if BOT_TOKEN == "":
    raise ValueError("bot token cannot be empty")
GREET_IMAGE_URL = "https://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/speaking-head.png"

# ---------------------------------------------------
# code
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(text=f"{markdown.hide_link(GREET_IMAGE_URL)} welcome {markdown.hbold(message.from_user.full_name)}\nuse '/help' for possible commands", parse_mode=ParseMode.HTML)

@dp.message(Command("help"))
async def handle_help(message: types.message):
    await message.answer(text="use '/hi <name>' to print 'hello, <name>'\nuse '/pick' for a selection dialog")

@dp.message(Command("hi"))
async def handle_hi(message: types.message, command: CommandObject):
    if command.args:
        await message.answer(text=f"hello, {command.args}")
    else:
        await message.answer(text="usage: /hi <name>")

@dp.message(Command("pick"))
async def handle_pick(message: types.message):
    kb = [
        [
            types.KeyboardButton(text="option 1"),
            types.KeyboardButton(text="option 2")
        ],
        [
            types.KeyboardButton(text="option 3"),
            types.KeyboardButton(text="option 4")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="select an option")
    await message.answer(text="select an option:", reply_markup=keyboard)

@dp.message(F.text.lower() == "option 1")
async def btn_answer(message: types.Message):
    await message.reply("you chose option 1")

@dp.message(F.text.lower() == "option 2")
async def btn_answer(message: types.Message):
    await message.reply("you chose option 2")

@dp.message(F.text.lower() == "option 3")
async def btn_answer(message: types.Message):
    await message.reply("you chose option 3")

@dp.message(F.text.lower() == "option 4")
async def btn_answer(message: types.Message):
    await message.reply("you chose option 4")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())