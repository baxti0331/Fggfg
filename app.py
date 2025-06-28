import os
import telebot
from flask import Flask, request

API_TOKEN = os.getenv('API_TOKEN')  # На Render должен быть API_TOKEN = твой токен

if not API_TOKEN:
    raise ValueError("Переменная окружения API_TOKEN не установлена")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

WEBHOOK_PATH = f"/{API_TOKEN}/"
WEBHOOK_URL = f"https://fggfg.onrender.com{WEBHOOK_PATH}"

@app.route("/", methods=['GET'])
def home():
    return "Bot is running!"

@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я активен и слушаю Webhook!")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=8080)