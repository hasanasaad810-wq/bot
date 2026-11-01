import os
import json
import telebot
from flask import Flask
from threading import Thread
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# التوكن الصحيح الخاص ببوتك
BOT_TOKEN = "9286755149:AAHopKGYhZhaCWyvC0U7vZV2FXXm0_jitKA"
ADMIN_ID = 1449111290

bot = telebot.TeleBot(BOT_TOKEN)
bot.remove_webhook()

ACCOUNTS_FILE = "ichancy_accounts.json"
user_states = {}

def load_accounts():
    if not os.path.exists(ACCOUNTS_FILE):
        return {}
    with open(ACCOUNTS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w", encoding="utf-8") as f:
        json.dump(accounts, f, ensure_ascii=False, indent=4)

# --- خادم ويب مصغر لمنع نوم البوت على Render ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()
# ---------------------------------------------

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("إنشاء حساب"), KeyboardButton("حساباتي"), KeyboardButton("حالة النظام"))
    bot.send_message(message.chat.id, "أهلاً بك في بوت إدارة الحسابات الخاص بك!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "حالة النظام":
        bot.send_message(message.chat.id, "البوت يعمل بكفاءة وجاهز لخدمتك 24/7 دون انقطاع.")
    else:
        bot.send_message(message.chat.id, "أهلاً بك، استخدم الأزرار بالأسفل للتنقل.")

if __name__ == "__main__":
    # تشغيل خادم الحفاظ على البوت نشطاً
    keep_alive()
    # تشغيل البوت
    bot.infinity_polling()
