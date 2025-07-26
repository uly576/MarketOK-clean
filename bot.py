import os
import telebot
from telebot import types
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# /start — головна команда
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id

    # Інлайн-кнопки
    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.add(
        types.InlineKeyboardButton("👋 Почати аналіз", callback_data="start_analysis"),
        types.InlineKeyboardButton("📄 Сценарій для сторіс", callback_data="story_script"),
        types.InlineKeyboardButton("ℹ️ Про бота", callback_data="about_bot")
    )

    # Reply-кнопки
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    reply_markup.add("📊 Аналіз поста", "ℹ️ Про бота")

    bot.send_message(
        chat_id,
        "Привіт! Обери, що хочеш зробити:",
        reply_markup=reply_markup,
        reply_markup_inline=inline_markup
    )

# Обробка інлайн-кнопок
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "start_analysis":
        bot.send_message(call.message.chat.id, "🧠 Запускаємо аналіз бізнесу!")
    elif call.data == "story_script":
        bot.send_message(call.message.chat.id, "📄 Надсилаю сценарій для сторіс...")
    elif call.data == "about_bot":
        bot.send_message(call.message.chat.id, "ℹ️ Я — бот для просування вашого бізнесу. Допомагаю з ідеями, контентом і більше!")

# Обробка reply-кнопок
@bot.message_handler(func=lambda message: True)
def reply_buttons_handler(message):
    if message.text == "📊 Аналіз поста":
        bot.send_message(message.chat.id, "Встав або надішли пост для аналізу.")
    elif message.text == "ℹ️ Про бота":
        bot.send_message(message.chat.id, "Я — твій маркетинговий помічник.")

bot.polling()









