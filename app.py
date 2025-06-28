import os
import telebot
from flask import Flask, request, abort

API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

clean_token = API_TOKEN.replace(':', '')
WEBHOOK_URL_BASE = 'https://fggfg-1.onrender.com'
WEBHOOK_URL_PATH = f"/{clean_token}/"

@app.route('/')
def index():
    return "Бот работает!"

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        abort(403)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот на вебхуках!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Ты написал: {message.text}")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    # НЕ вызываем app.run() при запуске под gunicorn