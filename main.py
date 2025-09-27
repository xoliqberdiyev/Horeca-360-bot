import asyncio, logging, sys, os, requests

from aiogram import Bot, Dispatcher, types, filters
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from dotenv import load_dotenv

load_dotenv()

TOKEN1 = os.getenv("TOKEN1")
TOKEN2 = os.getenv("TOKEN2")
BACKEND_URL = os.getenv("BACKEND_URL")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))  

bot1 = Bot(token=TOKEN1)
bot2 = Bot(token=TOKEN2)
dp1 = Dispatcher()
dp2 = Dispatcher()

class CodeStates(StatesGroup):
    phone = State()
    full_name = State()

class Broadcast(StatesGroup):
    waiting_for_message = State()



@dp2.message(filters.CommandStart())
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


@dp2.message(CodeStates.phone)
async def get_code(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    await message.answer('Ims Familiyangizni kirting:')
    await state.set_state(CodeStates.full_name)


@dp2.message(CodeStates.full_name)
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


@dp1.message(filters.Command(commands=['web_app']))
async def start_handler(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="Open",
                web_app=WebAppInfo(url="https://agro365.vercel.app")
            )]
        ],
        resize_keyboard=True
    )
    await message.answer("Salom! Web Appni ochish uchun tugmani bosing 👇", reply_markup=keyboard)


@dp1.message(filters.Command("send"))
async def start_broadcast(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ Sizda ruxsat yo‘q")

    await message.answer("Yubormoqchi bo‘lgan xabaringizni kiriting:")
    await state.set_state(Broadcast.waiting_for_message)


@dp1.message(Broadcast.waiting_for_message)
async def broadcast_message(message: types.Message, state: FSMContext):
    msg = message.text
    count = 0
    url = f'{BACKEND_URL}/api/v1/accounts/user/list/'
    res = requests.get(url)
    for chat_id in res.json():
        if chat_id['tg_id'] == ADMIN_ID:
            continue
        try:
            await bot1.send_message(chat_id['tg_id'], msg)
            count += 1
        except Exception as e:
            print(f"Xato {chat_id['tg_id']}: {e}")

    await message.answer(f"✅ {count} ta foydalanuvchiga yuborildi")
    await state.clear()



async def main():
    await asyncio.gather(
        dp1.start_polling(bot1),
        dp2.start_polling(bot2),
    )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())