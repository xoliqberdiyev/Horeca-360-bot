import asyncio, logging, sys, os, requests

from aiogram import Bot, Dispatcher, types, filters
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

TOKEN = "8043593409:AAEC4GfxOyfv9LmbfLiwU7_g-mdtuj3y8rI"
BACKEND_URL = 'https://agro.felixits.uz/'
bot = Bot(token=TOKEN)
dp = Dispatcher()

class CodeStates(StatesGroup):
    phone = State()
    full_name = State()


@dp.message(filters.CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    url = f"{BACKEND_URL}/api/v1/orders/supplier/{message.from_user.id}/"
    res = requests.get(url)
    if res.status_code == 404:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="📞 Telefon raqamni yuborish", request_contact=True)]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        await message.answer(
            "Assalomu alaykum! Iltimos, telefon raqamingizni yuboring:",
            reply_markup=keyboard
        )
        await state.set_state(CodeStates.phone)
    else:
        await message.answer("Salom")
        await state.clear()


@dp.message(CodeStates.phone)
async def get_code(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    await message.answer('Ims Familiyangizni kirting:')
    await state.set_state(CodeStates.full_name)


@dp.message(CodeStates.full_name)
async def get_code(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    url = f'{BACKEND_URL}/api/v1/orders/supplier/create/'
    data = await state.get_data()
    body = {
        'phone': data.get('phone'),
        'full_name': data.get('full_name'),
        'tg_id': message.from_user.id
    }
    res = requests.post(url, data=body)
    if res.status_code == 200:
        await message.answer("Raxmat")
        await state.clear()
    else:
        await message.answer(res.json())


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
