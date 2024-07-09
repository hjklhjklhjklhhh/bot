# ---------------------------------------------------
# modules
import asyncio
import datetime
import logging
import random
import requests
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandObject, CommandStart, Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import markdown
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from dotenv import load_dotenv

from openai import OpenAI

# ---------------------------------------------------
# constants
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if BOT_TOKEN == "":
    raise ValueError("bot token cannot be empty")
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
if OPENWEATHERMAP_API_KEY == "":
    raise ValueError("api key cannot be empty")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
if NEWSAPI_KEY == "":
    raise ValueError("api key cannot be empty")

FAKESTORE_PRODUCTS_URL = 'https://fakestoreapi.com/products'
FAKESTORE_CATEGORIES_URL = 'https://fakestoreapi.com/products/categories'
FAKESTORE_PRODUCTS_BY_CATEGORY_URL = 'https://fakestoreapi.com/products/category/{}'
GREET_IMAGE_URL = "https://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/speaking-head.png"

# ---------------------------------------------------
# code
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_categories():
    return requests.get(FAKESTORE_CATEGORIES_URL).json()

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    await message.answer(f"{markdown.hide_link(GREET_IMAGE_URL)} welcome {markdown.hbold(message.from_user.full_name)}\nuse '/help' for possible commands", parse_mode=ParseMode.HTML)

@dp.message(Command("help"))
async def handle_help(message: types.message):
    await message.answer("""use '/fakestore' to list products from different categories
    use '/hi <name>' to print 'hello, <name>'
    use '/info' for information about the bot
    use '/news <topic>' for news on <topic>
    use '/pick' for an option selector
    use '/picknum' for a number selector
    use '/pickrequest' for a request selector
    use '/random <min> <max> to get a button to generate a random number between <min> and <max> (inclusive)
    use '/randomword' for a random word
    use '/srandom' to generate a true random number between 0 and 255 (inclusive)
    use '/weather <location>' for weather info on <location>""")

@dp.message(Command("fakestore"))
async def handle_fakestore(message: types.message):
    builder = ReplyKeyboardBuilder()
    for category in get_categories():
        builder.row(types.KeyboardButton(text=category))
    await message.answer("select a category:", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(Command("hi"))
async def handle_hi(message: types.message, command: CommandObject):
    if command.args:
        await message.answer(f"hello, {command.args}")
    else:
        await message.answer("usage: /hi <name>")

@dp.message(Command("info"))
async def handle_info(message: types.Message):
    repo_btn = InlineKeyboardButton(text="GitHub repository", url="https://github.com/hjklhjklhjklhhh/bot")
    author_btn = InlineKeyboardButton(text="author", url="https://github.com/hjklhjklhjklhhh")
    markup = InlineKeyboardMarkup(inline_keyboard=[[repo_btn, author_btn]])
    await message.answer("visit the GitHub repo for info", reply_markup=markup)

@dp.message(Command("prompt"))
async def handle_prompt(message: types.message, command: CommandObject):
    if command.args:
        args = command.args.split()
        if len(args) >= 1:
            query = ' '.join(args)
            client = OpenAI()
            completion = client.chat.completions.create(
                model="text-davinci-003",
                messages=[
                    {"role": "user", "content": query}
                ]
            )
            await message.reply(completion.choices[0].message)
        else:
            await message.answer("usage: /prompt <prompt>")
    else:
        await message.answer("usage: /prompt <prompt>")

@dp.message(Command("news"))
async def handle_news(message: types.message, command: CommandObject):
    if command.args:
        args = command.args.split()
        if len(args) >= 1:
            try:
                query = ' '.join(args)
                r = requests.get(f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWSAPI_KEY}")
                data = r.json()

                if data["status"] == "ok":
                    articles = data["articles"][:3]
                    news_text = f"*** Latest news about '{query}': ***\n"
                    for article in articles:
                        news_text += f"- {article['title']}\n  {article['url']}\n"
                    await message.reply(news_text)
                else:
                    await message.reply("an error occurred.")
            except:
                await message.reply("an error occurred.")
        else:
            await message.answer("usage: /news <topic>")
    else:
        await message.answer("usage: /news <topic>")


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
    await message.answer("select an option:", reply_markup=keyboard)

@dp.message(Command("picknum"))
async def handle_picknum(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer("select a number:", reply_markup=builder.as_markup(resize_keyboard=True))

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

    await message.answer("select a request:", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(Command("random"))
async def handle_random(message: types.Message, command: CommandObject):
    if command.args:
        args = command.args.split()
        if len(args) == 2:
            builder = InlineKeyboardBuilder()
            builder.add(types.InlineKeyboardButton(text="generate", callback_data=args[0] + "," + args[1]))
            await message.answer(f"press the button to get a random number between {args[0]} and {args[1]}", reply_markup=builder.as_markup())
        else:
            await message.answer("usage: /random <min> <max>")
    else:
        await message.answer("usage: /random <min> <max>")

@dp.message(Command("randomword"))
async def handle_randomword(message: types.Message):
    try:
        r = requests.get("https://random-word-api.herokuapp.com/word")
        data = r.json()
        await message.reply(data[0])
    except:
        await message.reply("an error occurred.")

@dp.message(Command("srandom"))
async def handle_srandom(message: types.Message):
    data = os.urandom(1)
    await message.reply(str(int.from_bytes(data, byteorder="little")))

@dp.message(Command("weather"))
async def handle_weather(message: types.Message, command: CommandObject):
    if command.args:
        args = command.args.split()
        if len(args) == 1:
            WEATHER_EMOJIS = {
                "Clear": "\U00002600",
                "Clouds": "\U00002601",
                "Rain": "\U00002614",
                "Drizzle": "\U00002614",
                "Thunderstorm": "\U000026A1",
                "Snow": "\U0001F328",
                "Mist": "\U0001F32B"
            }

            try:
                r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={args[0]}&appid={OPENWEATHERMAP_API_KEY}&units=metric")
                data = r.json()

                city = data["name"]
                cur_weather = data["main"]["temp"]

                weather_description = data["weather"][0]["main"]
                if weather_description in WEATHER_EMOJIS:
                    wd = weather_description + WEATHER_EMOJIS[weather_description]
                else:
                    wd = weather_description

                humidity = data["main"]["humidity"]
                pressure = data["main"]["pressure"]
                wind = data["wind"]["speed"]
                sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
                sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
                length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                    data["sys"]["sunrise"])

                await message.reply(f"*** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} ***\n"
                      f"location: {city}\ntemperature: {cur_weather}°C {wd}\n"
                      f"humidity: {humidity}%\npressure: {pressure} hPa\nWind: {wind} m/s\n"
                      f"sunrise: {sunrise_timestamp}\nsunset: {sunset_timestamp}\nday length: {length_of_the_day}\n"
                      )
            except:
                await message.reply("an error occurred.")
        else:
            await message.answer("usage: /weather <location>")
    else:
        await message.answer("usage: /weather <location>")

@dp.message(lambda message: message.text in get_categories())
async def fakestore_answer(message: types.Message):
    try:
        r = requests.get(FAKESTORE_PRODUCTS_BY_CATEGORY_URL.format(message.text))
        data = r.json()
        for p in data:
            await message.answer_photo(photo=p['image'],
                    caption=f"*** product: {p['title']} ***\n"
                    f"price: {p['price']}\n"
                    f"description: {p['description']}\n"
                    f"rating: {p['rating']['rate']}, count: {p['rating']['count']}")
    except:
        await message.reply("an error occurred.")

@dp.message(F.text.lower().regexp("option [1-4]"))
async def pick_answer(message: types.Message):
    await message.reply(f"you chose the option {message.text}")

@dp.message(F.text.regexp(r"\b([1-9]|1[0-6])\b"))
async def picknum_answer(message: types.Message):
    await message.reply(f"you chose the number {message.text}")

@dp.callback_query(F.data.regexp(r"\b\d+,\d+\b"))
async def random_answer(callback: types.CallbackQuery):
    vals = callback.data.split(",")
    await callback.message.answer(str(random.randint(int(vals[0]), int(vals[1]))))

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())