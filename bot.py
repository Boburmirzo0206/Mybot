from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "7601461316:AAEE7VyTdwOhWjoSBznpkW_JFtS5K-59WB4"  # Oxirgi 4 raqamni o'zingiz qo'shing
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Foydalanuvchilarning tanlagan tilini saqlash
user_languages = {}

# 1. InlineKeyboard: Til tanlash
def get_language_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    )
    return keyboard

# 2. ReplyKeyboard: Asosiy tugmalar
def get_main_keyboard(lang):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    if lang == "uz":
        keyboard.add(KeyboardButton("Ob-havo"), KeyboardButton("Valyuta kurslari"))
        keyboard.add(KeyboardButton("Sozlamalar"), KeyboardButton("🌍 Tilni o‘zgartirish"))
    elif lang == "ru":
        keyboard.add(KeyboardButton("Погода"), KeyboardButton("Курсы валют"))
        keyboard.add(KeyboardButton("Настройки"), KeyboardButton("🌍 Изменить язык"))
    elif lang == "en":
        keyboard.add(KeyboardButton("Weather"), KeyboardButton("Exchange rates"))
        keyboard.add(KeyboardButton("Settings"), KeyboardButton("🌍 Change language"))
    return keyboard

# 3. /start - Bot ishga tushganda
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Tilni tanlang | Выберите язык | Select a language",
        reply_markup=get_language_keyboard()
    )

# 4. Tilni tanlash va saqlash
@dp.callback_query_handler(lambda c: c.data.startswith('lang_'))
async def process_language_selection(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    lang = callback_query.data.split("_")[1]
    user_languages[user_id] = lang  # Foydalanuvchining tilini saqlaymiz

    texts = {
        "uz": "Siz O‘zbek tilini tanladingiz.",
        "ru": "Вы выбрали русский язык.",
        "en": "You have selected English."
    }

    # ReplyKeyboard tugmalarini faqat endi qo‘shamiz
    await bot.send_message(user_id, texts[lang], reply_markup=get_main_keyboard(lang))

# 5. "Tilni o‘zgartirish" tugmasi bosilganda
@dp.message_handler(lambda message: message.text in ["🌍 Tilni o‘zgartirish", "🌍 Изменить язык", "🌍 Change language"])
async def change_language(message: types.Message):
    await message.reply(
        "Tilni tanlang | Выберите язык | Select a language",
        reply_markup=get_language_keyboard()
    )

# **Botni ishga tushirish**
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
