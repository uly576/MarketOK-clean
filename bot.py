import os
import telebot
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# Простий список для визначення цільової аудиторії за ключовими словами
niche_audiences = {
    "аксесуари": "Молодь 16–35 років, власники iPhone, жителі міст, слідкують за трендами",
    "косметика": "Жінки 18–45 років, зацікавлені в догляді за собою, інстаграм-користувачі",
    "одяг": "Чоловіки і жінки 18–35 років, цінують стиль, онлайн-шопінг",
    "курси": "Дорослі 20–40 років, хочуть прокачати навички, шукають саморозвиток",
    "дитячі товари": "Мами 25–40 років, турботливі, активні в соцмережах",
}

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привіт! 🤖 Я допоможу придумати контент для просування твого бізнесу. Напиши, що ти продаєш або яку послугу надаєш.")

@bot.message_handler(func=lambda m: True)
def handle_business_info(message):
    business = message.text.lower()
    
    # Визначення цільової аудиторії
    audience = "Люди, зацікавлені у вашому продукті."
    for keyword, target in niche_audiences.items():
        if keyword in business:
            audience = target
            break

    # Відповіді бота
    bot.send_message(message.chat.id, f"🎯 Цільова аудиторія для вашого бізнесу:\n{audience}")

    content = f"📝 Контент-ідея:\nРозкажіть, як ваш продукт вирішує проблему клієнта. Наприклад: \"Чому наші {business} — must-have у 2025 році?\""
    tiktok = f"🎥 Ідея для TikTok:\nПокажіть коротке відео з процесом використання або до/після з вашим продуктом ({business})."

    bot.send_message(message.chat.id, content)
    bot.send_message(message.chat.id, tiktok)

if __name__ == '__main__':
    bot.polling(none_stop=True)
