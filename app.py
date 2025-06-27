import os
import telebot
from flask import Flask, request

API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
    raise ValueError("Ошибка: переменная окружения API_TOKEN не установлена")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

WEBHOOK_URL_BASE = 'https://fggfg.onrender.com'  # твой домен
WEBHOOK_URL_PATH = f"/{API_TOKEN}/"

@app.route("/")
def home():
    return "Bot is running!"

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Добро пожаловать.")
    bot.send_message(message.chat.id, "Я бот, который отвечает на твои сообщения.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, "Спасибо за сообщение!")
    bot.send_message(message.chat.id, "Как у тебя дела?")
    bot.send_message(message.chat.id, "Если нужно, пиши ещё!")
    bot.send_message(message.chat.id, "Хорошего дня!")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    app.run(host="0.0.0.0", port=8080)