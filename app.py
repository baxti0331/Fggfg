import os
import telebot
from flask import Flask, request

API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

WEBHOOK_URL_PATH = f"/{API_TOKEN}/"

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот на вебхуках!")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=f"https://fggfg.onrender.com{WEBHOOK_URL_PATH}")
    app.run(host="0.0.0.0", port=8080)