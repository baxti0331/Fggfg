import os
import telebot
from flask import Flask, request, abort

API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
    raise RuntimeError("Ошибка: переменная окружения API_TOKEN не установлена")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

clean_token = API_TOKEN.replace(':', '')
WEBHOOK_URL_BASE = 'https://fggfg-1.onrender.com'  # замени на свой URL Render
WEBHOOK_URL_PATH = f"/{clean_token}/"

@app.route('/')
def index():
    return "Бот запущен и готов к работе!"

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        print(f"Получен запрос: {json_string}")
        update = telebot.types.Update.de_json(json_string)
        try:
            bot.process_new_updates([update])
            print("Апдейт обработан успешно")
        except Exception as e:
            print(f"Ошибка при обработке апдейта: {e}")
        return 'OK', 200
    else:
        abort(403)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(f"Команда /start от пользователя {message.chat.id}")
    try:
        bot.send_message(message.chat.id, "Привет! Я бот на вебхуках с логами.")
        print("Ответ отправлен успешно")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")

if __name__ == '__main__':
    print("Удаляю старый вебхук...")
    bot.remove_webhook()
    print("Устанавливаю новый вебхук...")
    success = bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    if success:
        print("Вебхук успешно установлен.")
    else:
        print("Ошибка при установке вебхука.")
    # app.run() не нужен, gunicorn будет запускать сервер