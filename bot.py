import asyncio
import os
import re
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ============ KALKULYATOR ============

# Har bir foydalanuvchi uchun kalkulyator holati
calc_sessions = {}


def get_calc_keyboard():
    """Kalkulyator tugmalari"""
    buttons = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"],
        ["C", "(", ")", "DEL"],
    ]
    keyboard = []
    for row in buttons:
        keyboard.append(
            [InlineKeyboardButton(text=btn, callback_data=f"calc_{btn}") for btn in row]
        )
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def safe_eval(expression: str) -> str:
    """Xavfsiz hisoblash - faqat raqamlar va arifmetik amallar"""
    # Faqat ruxsat etilgan belgilar
    allowed = re.compile(r'^[\d\+\-\*\/\.\(\)\s]+$')
    if not allowed.match(expression):
        return "Xato!"

    try:
        # Xavfsiz hisoblash
        result = eval(expression, {"__builtins__": {}}, {})
        # Natijani chiroyli formatlash
        if isinstance(result, float):
            if result == int(result):
                return str(int(result))
            return f"{result:.6f}".rstrip("0").rstrip(".")
        return str(result)
    except ZeroDivisionError:
        return "Nolga bo'lish mumkin emas!"
    except Exception:
        return "Xato!"


# ============ HANDLERS ============


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Botni ishga tushirish"""
    await message.answer(
        "Assalomu alaykum! Men kalkulyator botman.\n\n"
        "Buyruqlar:\n"
        "/calc - Kalkulyatorni ochish\n"
        "/help - Yordam\n\n"
        "Yoki to'g'ridan-to'g'ri matematik ifoda yozing:\n"
        "Masalan: 2+2, 10*5, (3+4)*2",
    )


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Yordam"""
    await message.answer(
        "Kalkulyator Bot - Yordam\n\n"
        "Tugmali kalkulyator: /calc\n\n"
        "Yoki to'g'ridan-to'g'ri yozing:\n"
        "  2 + 2\n"
        "  10 * 5\n"
        "  (3 + 4) * 2\n"
        "  100 / 25\n\n"
        "Qo'llab-quvvatlanadigan amallar:\n"
        "  + qo'shish\n"
        "  - ayirish\n"
        "  * ko'paytirish\n"
        "  / bo'lish\n"
        "  () qavslar",
    )


@dp.message(Command("calc"))
async def cmd_calc(message: types.Message):
    """Kalkulyatorni ochish"""
    user_id = message.from_user.id
    calc_sessions[user_id] = ""

    await message.answer(
        "Kalkulyator\n\n"
        "Ekran: _",
        reply_markup=get_calc_keyboard(),
    )


@dp.callback_query(F.data.startswith("calc_"))
async def calc_callback(callback: CallbackQuery):
    """Kalkulyator tugmalari bosilganda"""
    user_id = callback.from_user.id
    btn = callback.data.replace("calc_", "")

    if user_id not in calc_sessions:
        calc_sessions[user_id] = ""

    expression = calc_sessions[user_id]

    if btn == "C":
        # Tozalash
        calc_sessions[user_id] = ""
        display = "_"
    elif btn == "DEL":
        # Oxirgi belgini o'chirish
        calc_sessions[user_id] = expression[:-1]
        display = calc_sessions[user_id] if calc_sessions[user_id] else "_"
    elif btn == "=":
        # Hisoblash
        if expression:
            result = safe_eval(expression)
            display = f"{expression} = {result}"
            # Natijani yangi ifoda sifatida saqlash
            if result not in ("Xato!", "Nolga bo'lish mumkin emas!"):
                calc_sessions[user_id] = result
            else:
                calc_sessions[user_id] = ""
        else:
            display = "_"
    else:
        # Raqam yoki operator qo'shish
        calc_sessions[user_id] = expression + btn
        display = calc_sessions[user_id]

    await callback.message.edit_text(
        f"Kalkulyator\n\n"
        f"Ekran: {display}",
        reply_markup=get_calc_keyboard(),
    )
    await callback.answer()


@dp.message(F.text.regexp(r'^[\d\+\-\*\/\.\(\)\s]+$'))
async def direct_calculation(message: types.Message):
    """To'g'ridan-to'g'ri matematik ifoda yozilganda"""
    expression = message.text.strip()
    result = safe_eval(expression)
    await message.answer(f"{expression} = {result}")


# ============ MAIN ============


async def main():
    print("Bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
