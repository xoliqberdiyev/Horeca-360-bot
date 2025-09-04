import asyncio, logging, sys, os, requests

from aiogram import Bot, Dispatcher, types, filters
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

TOKEN = "8147952177:AAEsR2ejafoKVb_OFcm6rEJAzUt_BKiOr5A"

bot = Bot(token=TOKEN)
dp = Dispatcher()

class CodeStates(StatesGroup):
    product_code = State()


@dp.message(filters.CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer("Assalomu alaykum! Iltimos, mahsulot kodni kiriting:")
    await state.set_state(CodeStates.product_code)


@dp.message(CodeStates.product_code)
async def get_code(message: types.Message, state: FSMContext):
    code = message.text
    await state.clear()
    url = f'https://horeca.felixits.uz/api/v1/products/set_tg_id/{code}/'
    res = requests.post(url, data={'tg_id': message.from_user.id})
    if res.status_code == 200:
        await message.answer("Raxmat")
    else:
        await message.answer("Mahsulot topilmadi, qayta urinib koring")


@dp.message(filters.Command(commands=['web_app']))
async def start_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="Open",
                web_app=WebAppInfo(url="https://agro360.vercel.app")
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
