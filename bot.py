import os
import telebot
from dotenv import load_dotenv
from datetime import datetime, timedelta
import openai

# Завантаження змінних середовища
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ініціалізація
bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_API_KEY

# Зберігання доступу для користувачів (7 днів)
user_access = {}

def has_access(user_id):
    now = datetime.now()
    if user_id in user_access:
        return now - user_access[user_id] <= timedelta(days=7)
    else:
        user_access[user_id] = now
        return True

# Генерація відповіді через OpenAI
def generate_promo_idea(business_description):
    prompt = (
        f"Опиши цільову аудиторію для бізнесу: {business_description}.\n"
        f"Згенеруй ідею просування в TikTok.\n"
        f"Придумай PDF-гайд як лід-магніт + текст для публікації.\n"
        f"Відповідай українською мовою, структуровано."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти досвідчений маркетолог."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=900,
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("OpenAI error:", e)
        return "⚠️ Сталася помилка при зверненні до OpenAI."

# Обробка команди /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Привіт! Я допоможу створити ідеї для просування твого бізнесу.\n"
        "Напиши, як він називається та чим займається 😊"
    )

# Команда для PDF-гайду
@bot.message_handler(commands=['гайд'])
def send_guide(message):
    try:
        with open("lead_magnet.pdf", "rb") as file:
            bot.send_document(message.chat.id, file)
    except Exception:
        bot.send_message(message.chat.id, "⚠️ Не вдалося надіслати гайд. Перевірте, чи файл lead_magnet.pdf існує.")

# Основна логіка бота
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id

    if not has_access(user_id):
        bot.send_message(
            message.chat.id,
            "⛔️ Безкоштовний доступ завершено. Щоб продовжити користуватись ботом, придбай підписку за $9."
        )
        return

    business = message.text
    bot.send_message(message.chat.id, "🔍 Аналізую ваш бізнес...")

    result = generate_promo_idea(business)
    bot.send_message(message.chat.id, result)
    bot.send_message(message.chat.id, "📎 Хочеш безкоштовний PDF-гайд? Напиши /гайд")

# Запуск бота
bot.polling()





