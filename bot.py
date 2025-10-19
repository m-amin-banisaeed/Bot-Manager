import json
import os
import asyncio
from threading import Lock
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# 🧩 تنظیمات اولیه
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "توکن_ربات_اینجا")
ADMIN_ID = 123456789
TASK_FILE = "tasks.json"
file_lock = Lock()

# 📁 تابع برای بارگذاری/ذخیره تسک‌ها
def load_tasks():
    try:
        with file_lock:
            with open(TASK_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except FileNotFoundError:
        return {}

def save_tasks(data):
    with file_lock:
        with open(TASK_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# 📱 /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🗓 Today Task", callback_data="today_task")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام 👋 یه گزینه انتخاب کن:", reply_markup=reply_markup)

# 🎯 دکمه Today Task
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "today_task":
        username = query.from_user.username
        if not username:
            await query.edit_message_text("یوزرنیم نداری! لطفاً توی تلگرام برای خودت username تنظیم کن 😅")
            return

        try:
            tasks = load_tasks().get(username, [])
            if tasks:
                task_list = "\n".join([f"- {t}" for t in tasks])
                await query.edit_message_text(f"✅ تسک‌های امروز @{username}:\n\n{task_list}")
            else:
                await query.edit_message_text("فعلاً هیچ تسکی برات ثبت نشده 😴")
        except Exception:
            await query.edit_message_text("مشکلی پیش اومد! بعداً دوباره امتحان کن 😓")

# 🧑‍💼 دستور تنظیم تسک
async def set_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("فقط ادمین می‌تونه این دستور رو بزنه 😎")
        return

    if len(context.args) < 2:
        await update.message.reply_text("فرمت اشتباهه!\nمثال: /settask aminhunter task1, task2, task3")
        return

    username = context.args[0].replace("@", "")
    try:
        await context.bot.get_chat(f"@{username}")
        tasks = " ".join(context.args[1:]).split(",")
        tasks = [t.strip() for t in tasks if t.strip()]
        data = load_tasks()
        data[username] = tasks
        save_tasks(data)
        await update.message.reply_text(f"✅ تسک‌ها برای @{username} ذخیره شدن.")
    except:
        await update.message.reply_text(f"کاربر @{username} پیدا نشد یا خطایی رخ داد!")

# 🗑 دستور حذف تسک
async def delete_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("فقط ادمین می‌تونه این دستور رو بزنه 😎")
        return

    if not context.args:
        await update.message.reply_text("یوزرنیم وارد کن!\nمثال: /deletetask aminhunter")
        return

    username = context.args[0].replace("@", "")
    data = load_tasks()
    if username in data:
        del data[username]
        save_tasks(data)
        await update.message.reply_text(f"🗑 تسک‌های @{username} حذف شدن.")
    else:
        await update.message.reply_text(f"تسکی برای @{username} پیدا نشد!")

# 🚀 اجرای ربات
async def main():
    try:
        # ساخت اپلیکیشن
        app = ApplicationBuilder().token(TOKEN).build()

        # اضافه کردن هندلرها
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("settask", set_task))
        app.add_handler(CommandHandler("deletetask", delete_task))
        app.add_handler(CallbackQueryHandler(button_handler))

        print("🤖 ربات روشن شد و منتظره...")

        # راه‌اندازی ربات
        await app.initialize()
        await app.start()
        await app.updater.start_polling()

        # منتظر ماندن تا ربات به‌صورت دستی متوقف بشه
        while True:
            await asyncio.sleep(1)  # جلوگیری از مصرف زیاد CPU

    except KeyboardInterrupt:
        print("🛑 ربات توسط کاربر متوقف شد.")
    except Exception as e:
        print(f"❌ خطا: {e}")
    finally:
        # اطمینان از توقف و خاموش شدن ربات
        if 'app' in locals():
            await app.updater.stop()  # توقف Updater
            await app.stop()         # توقف اپلیکیشن
            await app.shutdown()     # خاموش کردن کامل
            print("🛑 ربات به‌درستی خاموش شد.")

if __name__ == "__main__":
    asyncio.run(main())
