import os
import telebot
from dotenv import load_dotenv
from datetime import datetime, timedelta
import openai

# Завантаження токенів
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ініціалізація бота
bot = telebot.TeleBot(TOKEN)
openai.api_key = OPENAI_API_KEY

# Зберігаємо дату початку використання
user_access = {}

def has_access(user_id):
    now = datetime.now()
    if user_id in user_access:
        started = user_access[user_id]
        return now - started <= timedelta(days=7)
    else:
        user_access[user_id] = now
        return True

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
                {"role": "system", "content": "Ти маркетолог."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print("OpenAI помилка:", e)
        return "⚠️ Сталася помилка при зверненні до OpenAI."

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Аналіз поста', 'Про бота')

    inline_markup = telebot.types.InlineKeyboardMarkup()
    inline_markup.row(
        telebot.types.InlineKeyboardButton("👋 Почати аналіз", callback_data="start_analysis"),
        telebot.types.InlineKeyboardButton("Сценарій для сторіс", callback_data="story_script")
    )

    bot.send_message(
        message.chat.id,
        "Привіт! Я допоможу з просуванням твого бізнесу 🧠\nОбери дію нижче 👇",
        reply_markup=markup
    )
    bot.send_message(message.chat.id, "Обери опцію нижче:", reply_markup=inline_markup)

@bot.message_handler(commands=['гайд'])
def send_guide(message):
    try:
        with open("lead_magnet.pdf", "rb") as file:
            bot.send_document(message.chat.id, file)
    except Exception:
        bot.send_message(message.chat.id, "⚠️ Не вдалося надіслати гайд. Перевір файл lead_magnet.pdf.")

@bot.message_handler(func=lambda m: m.text == 'Аналіз поста')
def analyze_post(message):
    bot.send_message(message.chat.id, "🔍 Надішли текст поста для аналізу...")

@bot.message_handler(func=lambda m: m.text == 'Про бота')
def about_bot(message):
    bot.send_message(
        message.chat.id,
        "🧠 Цей бот створений для допомоги в просуванні малого бізнесу.\n"
        "Він генерує ідеї, тексти, лід-магніти та допомагає з продажами.\n"
        "🚀 На базі OpenAI (ChatGPT)."
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    if call.data == "start_analysis":
        bot.send_message(call.message.chat.id, "✏️ Напиши, чим займається твій бізнес.")
    elif call.data == "story_script":
        bot.send_message(call.message.chat.id, "📚 Сценарій для сторіс доступний через /гайд")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.from_user.id

    if not has_access(user_id):
        bot.send_message(
            message.chat.id,
            "⛔️ Безкоштовний доступ завершено. Придбай підписку за $9 на місяць."
        )
        return

    business = message.text
    bot.send_message(message.chat.id, "🔍 Аналізую ваш бізнес...")

    result = generate_promo_idea(business)
    bot.send_message(message.chat.id, result)

    bot.send_message(message.chat.id, "📎 Хочеш безкоштовний PDF? Напиши /гайд")

bot.polling()











