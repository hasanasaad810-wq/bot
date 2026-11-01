import json
import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# التوكن الصحيح للبوت والأيدي الخاص بك
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

# القائمة الرئيسية (تتضمن أزرارك القديمة والجديدة معا)
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("📥 إنشاء حساب iChancy"), KeyboardButton("👤 معلومات الحساب"))
    markup.row(KeyboardButton("💳 شحن رصيد"), KeyboardButton("🛠 الدعم الفني"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "مرحباً بك! اختر ما تحتاجه من القائمة أدناه:",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id_str = str(message.from_user.id)
    accounts = load_accounts()
    text = message.text

    if text == "📥 إنشاء حساب iChancy":
        if user_id_str in accounts:
            acc = accounts[user_id_str]
            bot.send_message(
                message.chat.id,
                f"⚠️ لديك حساب مسجل مسبقاً ولا يمكنك إنشاء حساب آخر!\n\n"
                f"👤 اسم المستخدم: {acc['username']}\n"
                f"🔑 كلمة المرور: {acc['password']}",
                reply_markup=main_menu()
            )
        else:
            user_states[user_id_str] = "waiting_for_ichancy_credentials"
            bot.send_message(
                message.chat.id,
                "📝 يرجى إرسال **الاسم** و**كلمة السر** التي ترغب بهما لحساب iChancy (في رسالة واحدة):\n\n"
                "مثال:\n`اسم_المستخدم كلمة_السر`",
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardRemove()
            )

    elif text == "👤 معلومات الحساب":
        if user_id_str in accounts:
            acc = accounts[user_id_str]
            bot.send_message(
                message.chat.id,
                f"📋 معلومات حسابك الحالي:\n\n"
                f"👤 اسم المستخدم: {acc['username']}\n"
                f"🔑 كلمة المرور: {acc['password']}",
                reply_markup=main_menu()
            )
        else:
            bot.send_message(
                message.chat.id,
                "❌ ليس لديك أي حساب مسجل بعد. اضغط على زر '📥 إنشاء حساب iChancy' للبدء.",
                reply_markup=main_menu()
            )

    elif user_states.get(user_id_str) == "waiting_for_ichancy_credentials":
        user_states.pop(user_id_str, None)
        
        admin_msg = (
            f"🔔 **طلب إنشاء حساب iChancy جديد!**\n\n"
            f"👤 اسم الزبون: {message.from_user.first_name}\n"
            f"🆔 الآيدي: `{message.from_user.id}`\n"
            f"🔗 المعرف: @{message.from_user.username or 'لا يوجد'}\n\n"
            f"📥 البيانات المطلوبة:\n{text}"
        )
        bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")

        accounts[user_id_str] = {
            "username": text,
            "password": "قيد الإنشاء من قبل الإدارة..."
        }
        save_accounts(accounts)

        bot.send_message(
            message.chat.id,
            "✅ تم إرسال طلبك إلى الإدارة بنجاح!\nسيتم إنشاء الحساب وإرسال التفاصيل لك فوراً.",
            reply_markup=main_menu()
        )
        
    elif text == "💳 شحن رصيد":
        bot.send_message(message.chat.id, "لشحن الرصيد، يرجى التواصل مع الإدارة.", reply_markup=main_menu())
        
    elif text == "🛠 الدعم الفني":
        bot.send_message(message.chat.id, "أهلاً بك، يرجى كتابة مشكلتك ليتم الرد عليك.", reply_markup=main_menu())

bot.polling(none_stop=True)
