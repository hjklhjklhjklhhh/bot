# ---------------------------------------------------
# modules
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
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
    await message.answer(text=f"{markdown.hide_link(GREET_IMAGE_URL)} welcome {markdown.hbold(message.from_user.full_name)}", parse_mode=ParseMode.HTML)

@dp.message(Command("help"))
async def handle_help(message: types.message):
    await message.answer(text="send any message to echo it back\nuse '/hi <name>' to print 'hello, <name>'\nuse '/pick' for a selection dialog")

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

@dp.message()
async def echo_message(message: types.Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("invalid message")
    #if message.text:
    #    await message.reply(text=message.text, entities=message.entities, parse_mode=None)
    #elif message.sticker:
    #    await message.reply_sticker(sticker=message.sticker.file_id)
    #elif message.photo:
    #    await message.reply_photo(photo=message.photo[0].file_id)
    #elif message.animation:
    #    await message.reply_animation(animation=message.animation.file_id)
    #else:
    #    await message.reply(text="invalid message")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())