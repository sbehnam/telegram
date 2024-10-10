
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters

# تنظیمات توکن بات
TOKEN = "8078556164:AAGvRk4pfutvyuhndvbgAxaEcyehOtpUy_o"
bot = telegram.Bot(token=TOKEN)

# ایجاد اپ Flask
app = Flask(__name__)

# تنظیم webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
        return 'ok'

# تنظیم dispatcher و فیلترها
dispatcher = Dispatcher(bot, None)

# تابع برای بررسی اینکه آیا کاربر مدیر یا مالک است
def is_user_admin(chat_id, user_id):
    admins = bot.get_chat_administrators(chat_id)
    for admin in admins:
        if admin.user.id == user_id:
            return True
    return False

# هندلر برای مدیریت پیام‌ها در تاپیک‌های مجاز
def handle_message(update, context):
    chat = update.effective_chat
    message = update.message
    user = message.from_user

    # فقط پیام‌های درون سوپرگروپ بررسی شود
    if chat and chat.type == 'supergroup':
        topic_name = chat.title  # عنوان تاپیک گروه

        # حذف پیام در صورت ارسال در تاپیکی غیر از "Discussion"
        if topic_name != "Discussion":
            # بررسی اینکه کاربر مدیر یا مالک نباشد
            if not is_user_admin(chat.id, user.id):
                # حذف پیام فقط اگر پیام جدید باشد
                if message.date > context.bot_data.get('start_time'):
                    bot.delete_message(chat_id=chat.id, message_id=message.message_id)

# ذخیره زمان شروع بات
dispatcher.bot_data['start_time'] = telegram.utils.helpers.datetime.datetime.utcnow()

# اضافه کردن هندلر به dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_message))

if __name__ == '__main__':
    app.run(debug=True)
