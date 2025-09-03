from aiogram import Bot, Dispatcher, types, filters
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import asyncio, logging, sys

TOKEN = "8147952177:AAEsR2ejafoKVb_OFcm6rEJAzUt_BKiOr5A"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(filters.Command(commands=['web_app']))
async def start_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="Open",
                web_app=WebAppInfo(url="https://agro360.vercel.app")  # Web app URL
            )]
        ],
        resize_keyboard=True
    )
    await message.answer("Salom! Web Appni ochish uchun tugmani bosing 👇", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
