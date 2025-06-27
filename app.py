import os
import telebot
from flask import Flask
import threading
import time
import requests

API_TOKEN = os.getenv('API_TOKEN')
if not API_TOKEN:
    raise ValueError("Ошибка: переменная окружения API_TOKEN не установлена")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

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

def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
        except Exception as e:
            print(f"Polling failed: {e}. Перезапуск через 5 секунд...")
            time.sleep(5)

def keep_alive():
    while True:
        try:
            requests.get("http://localhost:8080/")
        except Exception as e:
            print(f"Keep-alive ping failed: {e}")
        time.sleep(300)  # Пинг раз в 5 минут

if __name__ == '__main__':
    threading.Thread(target=run_bot, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    # НЕ запускаем app.run(), сервер запустится через gunicorn
