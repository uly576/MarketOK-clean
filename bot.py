import os
import telebot
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# Зберігаємо дату початку використання
user_access = {}

# Заготовка функції для перевірки 7 днів безкоштовного доступу
def has_access(user_id):
    now = datetime.now()
    if user_id in user_access:
        started = user_access[user_id]
        if now - started > timedelta(days=7):
            return False
        return True
    else:
        user_access[user_id] = now
        return True

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привіт! Я допоможу створити ідеї для просування твого бізнесу. Напиши, як він називається та чим займається?")
    try:
        with open("lead_magnet.pdf", "rb") as file:
            bot.send_document(message.chat.id, file)
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Не вдалося надіслати гайд. Перевірте наявність файлу lead_magnet.pdf")

@bot.message_handler(commands=['гайд'])
def send_guide(message):
    try:
        with open("lead_magnet.pdf", "rb") as file:
            bot.send_document(message.chat.id, file)
    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Не вдалося надіслати гайд. Перевірте наявність файлу lead_magnet.pdf")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id

    if not has_access(user_id):
        bot.send_message(message.chat.id, "⛔️ Безкоштовний доступ завершено. Щоб продовжити користуватись ботом, придбай підписку за $9.")
        return

    business = message.text

    # Генеруємо приклад аудиторії
    audience = (
        "1. Жінки 25–35 років, які шукають нові способи догляду за собою та цікавляться wellness-тематикою.\n"
        "2. Чоловіки 30–45 років, що займаються бізнесом і потребують інструментів для ефективного планування.\n"
        "3. Молодь 18–25 років, активні в TikTok та Instagram, шукають легкий заробіток або підробіток."
    )

    # Ідея для Instagram або TikTok
    idea = (
        "🎯 Ідея для TikTok: Покажи 'до і після' результат від використання твого продукту/послуги. Додай реальні цифри або відгуки."
    )

    # Лід-магніт приклад
    lead_magnet = (
        "🎁 Лід-магніт: Безкоштовний PDF-гайд \"5 помилок, які вбивають продажі в Instagram\".\n"
        "✍️ Текст для публікації: \"Твій Instagram працює, але не продає? Завантаж гайд і дізнайся, що ти робиш не так. Посилання в описі профілю!\""
    )

    response = (
        f"✅ Опис бізнесу отримано.\n\n"
        f"📌 Цільова аудиторія для вашого бізнесу:\n{audience}\n\n"
        f"📢 Ідея для просування:\n{idea}\n\n"
        f"💡 Лід-магніт:\n{lead_magnet}"
    )

    bot.send_message(message.chat.id, response)

bot.polling()

