# ---------------------------------------------------
# modules
import asyncio
import logging

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandObject, CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder

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
    await message.answer(text="""use '/hi <name>' to print 'hello, <name>'
    use '/info' for information about the bot
    use '/pick' for an option selector
    use '/picknum' for a number selector
    use '/pickrequest' for a request selector""")

@dp.message(Command("hi"))
async def handle_hi(message: types.message, command: CommandObject):
    if command.args:
        await message.answer(text=f"hello, {command.args}")
    else:
        await message.answer(text="usage: /hi <name>")

@dp.message(Command("info"))
async def handle_info(message: types.Message):
    repo_btn = InlineKeyboardButton(text="GitHub repository", url="https://github.com/hjklhjklhjklhhh/bot")
    author_btn = InlineKeyboardButton(text="author", url="https://github.com/hjklhjklhjklhhh")
    markup = InlineKeyboardMarkup(inline_keyboard=[[repo_btn, author_btn]])
    await message.answer(text="visit the GitHub repo for info", reply_markup=markup)

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

@dp.message(Command("picknum"))
async def handle_picknum(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(text="select a number:", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(Command("pickrequest"))
async def handle_pickrequest(message: types.Message):
    builder = ReplyKeyboardBuilder()

    builder.row(
        types.KeyboardButton(text="request location", request_location=True),
        types.KeyboardButton(text="request contact", request_contact=True)
    )

    builder.row(
        types.KeyboardButton(text="request poll", request_poll=types.KeyboardButtonPollType(type="poll"))
    )

    builder.row(
        types.KeyboardButton(text="request selection for user", request_user=types.KeyboardButtonRequestUser(request_id=1)),
        types.KeyboardButton(text="request selection for premium user", request_user=types.KeyboardButtonRequestUser(request_id=2, user_is_premium=True))
    )

    builder.row(
        types.KeyboardButton(text="request selection for supergroup with forum", request_chat=types.KeyboardButtonRequestChat(request_id=3, chat_is_channel=False, chat_is_forum=True))
    )

    await message.answer(text="select a request:", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text.lower().regexp("option [1-4]"))
async def pick_answer(message: types.Message):
    await message.reply(f"you chose the option {message.text}")

@dp.message(F.text.regexp(r"\b([1-9]|1[0-6])\b"))
async def picknum_answer(message: types.Message):
    await message.reply(f"you chose the number {message.text}")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())