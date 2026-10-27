import asyncio
import random
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# ─── НАСТРОЙКИ ───
BOT_TOKEN = os.getenv("BOT_TOKEN", "8972105663:AAEGZi5WGqU0BIHXuVZvugiuGLN51d10-SE")
ADMIN_ID = 8529996312
SUPPORT_LINK = "https://t.me/soakxk"
IMAGE_PATH = "snow.jpg"
FAKE_DELETED_ACCOUNT = "karma_nastignet_vsex18"

VALID_KEYS = ["PROMO-2024", "VIP-ACCESS"]

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    waiting_username = State()
    waiting_key = State()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ─── КЛАВИАТУРЫ ───

def main_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="🛠 Техподдержка", url=SUPPORT_LINK)
    builder.button(text="💥 zнос аккаунта", callback_data="start_snos")
    builder.button(text="🔑 Активировать ключ", callback_data="activate")
    builder.adjust(1)
    return builder.as_markup()

def confirm_kb(username: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да, снести к хуям", callback_data=f"confirm_snos:{username}")
    builder.button(text="❌ Отмена", callback_data="cancel")
    builder.adjust(1)
    return builder.as_markup()

# ─── ХЕНДЛЕРЫ ───

@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    text = (
        "❄️ <b>Добро пожаловать в Z-NOSER</b> ❄️\n\n"
        "Закрытый инструмент для сноса аккаунтов.\n"
        "Выбери действие:"
    )
    try:
        photo = types.FSInputFile(IMAGE_PATH)
        await message.answer_photo(photo=photo, caption=text, reply_markup=main_menu_kb(), parse_mode="HTML")
    except Exception:
        await message.answer(text, reply_markup=main_menu_kb(), parse_mode="HTML")

@dp.callback_query(F.data == "activate")
async def activate_key(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text("🔑 Введи ключ доступа:")
    await state.set_state(Form.waiting_key)

@dp.message(Form.waiting_key)
async def process_key(message: types.Message, state: FSMContext):
    key = message.text.strip().upper()
    if key in VALID_KEYS:
        await message.answer("✅ Ключ активирован! Доступ к сносу открыт.")
    else:
        await message.answer("❌ Неверный ключ.")
    await state.clear()
    await message.answer("Возврат в меню:", reply_markup=main_menu_kb())

@dp.callback_query(F.data == "start_snos")
async def start_snos(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text("🎯 Введи username цели (с @):")
    await state.set_state(Form.waiting_username)

@dp.message(Form.waiting_username)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text.strip()
    if not username.startswith("@"):
        await message.answer("❌ Ошибка. Юзернейм должен начинаться с @. Попробуй ещё раз:")
        return
    await state.update_data(target=username)
    await message.answer(
        f"Цель: <b>{username}</b>\nПодтверждаешь?",
        reply_markup=confirm_kb(username),
        parse_mode="HTML"
    )
    await state.set_state(None)

@dp.callback_query(F.data.startswith("confirm_snos:"))
async def confirm_snos(callback: types.CallbackQuery):
    await callback.answer("Начинаю...")
    target = callback.data.split(":")[1]
    
    steps = [1, 6, 14, 28, 54, 89, 150, 300, 500, 850, 1200, 2000, 3500, 5700, 8900, 10000]
    
    msg = await callback.message.edit_text(
        f"⚙️ <i>Отправка жалоб:</i> <b>{steps[0]}</b>", 
        parse_mode="HTML"
    )
    await asyncio.sleep(1.2)
    
    for count in steps[1:]:
        try:
            await msg.edit_text(
                f"⚙️ <i>Отправка жалоб:</i> <b>{count}</b>", 
                parse_mode="HTML"
            )
        except Exception:
            pass
        await asyncio.sleep(1.0)

    await msg.edit_text(
        f"✅ <b>ЖАЛОБЫ ОТПРАВЛЕНЫ</b>\n\n"
        f"📊 Всего: <b>10000</b>",
        parse_mode="HTML"
    )
    await asyncio.sleep(1.5)

    logs = [
        "🌐 <i>Подключение к серверам Telegram...</i>",
        "🛡 <i>Обход защиты 2FA...</i>",
        "💉 <i>Инъекция в базу данных...</i>",
        "📡 <i>Маскировка IP-адреса...</i>",
        "🧹 <i>Удаление сообщений в чате...</i>",
    ]
    
    for log in logs:
        await msg.edit_text(log, parse_mode="HTML")
        await asyncio.sleep(1.5)

    final_text = (
        f"❄️ <b>АККАУНТ ЗАМОРОЖЕН</b> ❄️\n\n"
        f"📉 Статус: <code>Удаленный аккаунт</code>\n"
        f"📊 Всего жалоб: <b>10000</b>\n"
        f"💀 Система: Telegram Anti-Fraud\n\n"
        f"<i>Аккаунт заблокирован. Перейди в чат, чтобы увидеть результат.</i>"
    )
    
    builder = InlineKeyboardBuilder()
    builder.button(text="💬 Перейти в чат", url=f"https://t.me/{FAKE_DELETED_ACCOUNT}")
    builder.button(text="↩️ В меню", callback_data="back_to_menu")
    builder.adjust(1)
    
    await msg.edit_text(final_text, reply_markup=builder.as_markup(), parse_mode="HTML")

@dp.callback_query(F.data == "cancel")
async def cancel(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Отменено.", reply_markup=main_menu_kb())

@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("привет. это zносер от @soakxk, выбирай функцию", reply_markup=main_menu_kb())

@dp.message(Command("genkey"))
async def gen_key(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    new_key = f"KEY-{random.randint(10000, 99999)}"
    VALID_KEYS.append(new_key)
    await message.answer(f"✅ Новый ключ: <code>{new_key}</code>", parse_mode="HTML")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
