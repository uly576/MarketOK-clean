import os
import telebot
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# Зберігаємо дату початку використання
user_access = {}

# Перевірка доступу протягом 7 днів
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

# Визначення бізнес-напряму з тексту
def detect_niche(text):
    text = text.lower()
    if "білизн" in text:
        return "postilna"
    if "одяг" in text:
        return "odyag"
    if "манікюр" in text or "брови" in text:
        return "beauty"
    if "косметика" in text:
        return "cosmetics"
    return "default"

# Відповіді для кожної ніші
niche_data = {
    "postilna": {
        "audience": (
            "1. Жінки 27–45 років, що цінують комфорт і естетику в домі.\n"
            "2. Молоді мами, які шукають безпечні тканини для дітей.\n"
            "3. Люди, що переїхали або роблять ремонт — хочуть оновити текстиль."
        ),
        "idea": (
            "🎥 TikTok ідея: Розпакування білизни + ASMR момент, коли її стелиш. Вкінці: 'А ти вже оновлював(ла) свою спальню?'"
        ),
        "lead": (
            "🎁 PDF-гайд: \"Як вибрати постільну білизну, яка служить роками\".\n"
            "✍️ Текст: \"Як не викидати гроші на тканину, яка сідає після прання? Ми зібрали поради в PDF. Завантаж безкоштовно 👇\""
        )
    },
    "default": {
        "audience": (
            "1. Жінки 25–35 років, які шукають нові ідеї для розвитку.\n"
            "2. Чоловіки 30–45 років, що займаються бізнесом.\n"
            "3. Молодь 18–25 років, активна в TikTok."
        ),
        "idea": (
            "🎯 Ідея для TikTok: Покажи 'до і після' від твого продукту/послуги."
        ),
        "lead": (
            "🎁 PDF-гайд: \"5 помилок, які вбивають продажі в Instagram\".\n"
            "✍️ Текст: \"Твій Instagram не продає? Завантаж гайд і дізнайся, що ти робиш не так.\""
        )
    }
}

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Привіт! Я допоможу створити ідеї для просування твого бізнесу.\n"
        "Напиши, як він називається та чим займається 😊"
    )

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
    niche = detect_niche(business)
    data = niche_data.get(niche, niche_data["default"])

    response = (
        f"✅ Опис бізнесу отримано.\n\n"
        f"📌 Цільова аудиторія:\n{data['audience']}\n\n"
        f"📢 Ідея для просування:\n{data['idea']}\n\n"
        f"💡 Лід-магніт:\n{data['lead']}"
    )

    response += "\n\n📎 Хочеш безкоштовний PDF-гайд? Напиши /гайд"
    bot.send_message(message.chat.id, response)

bot.polling()

