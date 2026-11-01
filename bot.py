import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# التوكن الخاص ببوتك
BOT_TOKEN = "9286755149:AAHa4vlDxauu1_SCtWPXMdBdKjbx053CzVE"
# الأيدي الخاص بك كمدير لتستقبل الإشعارات والطلبات عليه
ADMIN_ID = 1449111290

bot = telebot.TeleBot(BOT_TOKEN)
bot.remove_webhook()

# ----------------- القائمة الرئيسية للمستخدم -----------------
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("💳 شحن رصيد"), KeyboardButton("💸 سحب أموال"))
    markup.row(KeyboardButton("📞 الدعم الفني"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        "أهلاً بك في منصة الخدمات الرقمية! اختر من القائمة أدناه:", 
        reply_markup=main_menu()
    )

# ----------------- طلب شحن الرصيد -----------------
@bot.message_handler(func=lambda msg: msg.text == "💳 شحن رصيد")
def deposit_request(message):
    msg = bot.send_message(message.chat.id, "أدخل المبلغ الذي ترغب بشحنه:")
    bot.register_next_step_handler(msg, process_deposit)

def process_deposit(message):
    amount = message.text
    user_info = f"👤 مستخدم: @{message.from_user.username or message.from_user.first_name} (ID: `{message.from_user.id}`)"
    
    # إرسال إشعار للمدير مع أزرار التحكم
    admin_markup = InlineKeyboardMarkup()
    admin_markup.row(
        InlineKeyboardButton("✅ قبول", callback_data=f"approve_dep_{message.from_user.id}_{amount}"),
        InlineKeyboardButton("❌ رفض", callback_data=f"reject_dep_{message.from_user.id}")
    )
    
    bot.send_message(
        ADMIN_ID, 
        f"📥 **طلب شحن جديد**\n\n{user_info}\n💰 المبلغ: {amount}", 
        parse_mode="Markdown", 
        reply_markup=admin_markup
    )
    bot.send_message(message.chat.id, "تم إرسال طلب الشحن إلى الإدارة لتمحيصه وتأكيده.")

# ----------------- طلب سحب الأموال -----------------
@bot.message_handler(func=lambda msg: msg.text == "💸 سحب أموال")
def withdraw_request(message):
    msg = bot.send_message(message.chat.id, "أدخل المبلغ المراد سحبه ورقم المحفظة:")
    bot.register_next_step_handler(msg, process_withdraw)

def process_withdraw(message):
    details = message.text
    user_info = f"👤 مستخدم: @{message.from_user.username or message.from_user.first_name} (ID: `{message.from_user.id}`)"
    
    admin_markup = InlineKeyboardMarkup()
    admin_markup.row(
        InlineKeyboardButton("✅ تم التحويل", callback_data=f"approve_with_{message.from_user.id}"),
        InlineKeyboardButton("❌ رفض الطلب", callback_data=f"reject_with_{message.from_user.id}")
    )
    
    bot.send_message(
        ADMIN_ID, 
        f"📤 **طلب سحب جديد**\n\n{user_info}\n📝 التفاصيل: {details}", 
        parse_mode="Markdown", 
        reply_markup=admin_markup
    )
    bot.send_message(message.chat.id, "تم استلام طلب السحب، سيتم المعالجة قريباً.")

# ----------------- معالجة قرارات المدير -----------------
@bot.callback_query_handler(func=lambda call: True)
def handle_admin_action(call):
    data = call.data.split("_")
    action = data[0]
    type_req = data[1]
    target_user_id = int(data[2])

    if action == "approve":
        amount_info = f" بمبلغ {data[3]}" if len(data) > 3 else ""
        bot.send_message(target_user_id, f"🎉 تم قبول طلبك{amount_info} بنجاح!")
        bot.answer_callback_query(call.id, "تم قبول الطلب وإشعار المستخدم.")
        bot.edit_message_text(f"{call.message.text}\n\n✅ **حالة الطلب: مقبول**", ADMIN_ID, call.message.message_id)
    
    elif action == "reject":
        bot.send_message(target_user_id, "❌ للأسف، تم رفض طلبك من قبل الإدارة.")
        bot.answer_callback_query(call.id, "تم رفض الطلب وإشعار المستخدم.")
        bot.edit_message_text(f"{call.message.text}\n\n❌ **حالة الطلب: مرفوض**", ADMIN_ID, call.message.message_id)

# ----------------- الدعم الفني -----------------
@bot.message_handler(func=lambda msg: msg.text == "📞 الدعم الفني")
def support(message):
    bot.send_message(message.chat.id, "لتواصل مباشر مع الدعم الفني، يرجى مراسلة الحساب: @YourSupportHandle")

bot.infinity_polling()
