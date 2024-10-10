import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# تنظیمات لاگینگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# توکن بات خود را وارد کنید
TOKEN = "YOUR_NEW_BOT_TOKEN"

# نام تاپیک مجاز
ALLOWED_TOPIC = "Discussion"

# فرمان شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("سلام! شما فقط در تاپیک 'Discussion' مجاز به ارسال پیام هستید.")

# هندلر پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    chat = message.chat

    # بررسی نوع چت
    if chat.type not in ['group', 'supergroup']:
        return  # فقط در گروه‌ها بررسی شود

    # بررسی اینکه آیا پیام در یک تاپیک خاص ارسال شده است
    if message.is_topic_message:
        topic_name = message.topic_name  # دریافت نام تاپیک

        # بررسی اینکه آیا فرستنده مدیر است
        member = await chat.get_member(message.from_user.id)
        if member.status in ['administrator', 'creator']:
            return  # مدیران مجاز به ارسال در همه تاپیک‌ها هستند

        # اگر تاپیک مجاز نباشد، پیام را حذف کن
        if topic_name != ALLOWED_TOPIC:
            try:
                await message.delete()
                logger.info(f"پیام از کاربر {message.from_user.id} در تاپیک '{topic_name}' حذف شد.")
            except Exception as e:
                logger.error(f"خطا در حذف پیام: {e}")

# تابع اصلی برای راه‌اندازی بات
def main():
    # ایجاد برنامه بات
    application = ApplicationBuilder().token(TOKEN).build()

    # افزودن هندلر فرمان شروع
    application.add_handler(CommandHandler("start", start))

    # افزودن هندلر پیام‌ها
    application.add_handler(MessageHandler(filters.ALL & ~filters.StatusUpdate.ALL, handle_message))

    # شروع به دریافت به‌روزرسانی‌ها
    application.run_polling()

if __name__ == '__main__':
    main()
