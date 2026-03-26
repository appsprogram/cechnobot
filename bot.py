# bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# ===== إعدادات البوت =====
TOKEN = os.getenv("TOKEN")  # توكن البوت في Railway Variables
ADMIN_ID = 7228888995

# رابط GitHub raw للملفات (ضع هنا الرابط الصحيح)
GITHUB_RAW = "https://raw.githubusercontent.com/appsprogram/cechnobot/main/media/"

# ===== القوائم =====
MAIN_MENU = [
    [InlineKeyboardButton("📊 عرض إجابتنا للطلاب", callback_data='answers')],
    [InlineKeyboardButton("📘 كيفية الاشتراك بمنصة ALEKS", callback_data='alek_help')],
    [InlineKeyboardButton("📩 التواصل معنا", callback_data='contact')]
]

ANSWERS_MENU = [
    [InlineKeyboardButton("📊 الإحصاء - ALEKS", callback_data='aleks')],
    [InlineKeyboardButton("📚 واجبات أخرى", callback_data='other')],
    [InlineKeyboardButton("🔙 رجوع", callback_data='home')]
]

BACK_BUTTON = [
    [InlineKeyboardButton("🔙 رجوع", callback_data='home')]
]

# ===== البداية =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً بك في بوت تكنو درس 👨‍💻\n"
        "بوت مساعد حول الاستفسارات...\n\n"
        "اختر من القائمة:",
        reply_markup=InlineKeyboardMarkup(MAIN_MENU)
    )

# ===== إرسال ملفات من GitHub =====
MEDIA_FILES = [
    "ALEKS1.jpg",
    "ALEKS_video.mp4",
    "other1.jpg",
    "help1.png",
    "help2.png",
    "help3.png"
]

async def send_media_by_prefix(context, chat_id, prefix):
    for f in MEDIA_FILES:
        if f.lower().startswith(prefix.lower()):
            url = GITHUB_RAW + f
            if f.endswith(".mp4"):
                await context.bot.send_video(chat_id=chat_id, video=url)
            else:
                await context.bot.send_photo(chat_id=chat_id, photo=url)

# ===== الأزرار =====
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "home":
        await query.edit_message_text(
            "القائمة الرئيسية:",
            reply_markup=InlineKeyboardMarkup(MAIN_MENU)
        )
    elif data == "answers":
        await query.edit_message_text(
            "اختر:",
            reply_markup=InlineKeyboardMarkup(ANSWERS_MENU)
        )
    elif data == "aleks":
        await send_media_by_prefix(context, query.message.chat.id, "aleks")
    elif data == "other":
        await send_media_by_prefix(context, query.message.chat.id, "other")
    elif data == "alek_help":
        # 1: صورة help1
        await context.bot.send_photo(
            chat_id=query.message.chat.id,
            photo=GITHUB_RAW + "help1.png",
            caption="هل عندك تطبيق التحقق؟"
        )
        # 2: تحميل تطبيق KAU Authenticator
        keyboard = [
            [InlineKeyboardButton("📱 iPhone", url="https://apps.apple.com")],
            [InlineKeyboardButton("🤖 Android", url="https://play.google.com")]
        ]
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text="تحميل تطبيق KAU Authenticator:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        # 3: التعليمات
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text="إذا لم تربط التطبيق:\nتواصل مع الدعم:\n+966126952209"
        )
        # 4 و5: صور help2 و help3
        await context.bot.send_photo(chat_id=query.message.chat.id, photo=GITHUB_RAW + "help2.png")
        await context.bot.send_photo(chat_id=query.message.chat.id, photo=GITHUB_RAW + "help3.png")
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text="🔙 للرجوع للقائمة استخدم الزر",
            reply_markup=InlineKeyboardMarkup(BACK_BUTTON)
        )
    elif data == "contact":
        await query.edit_message_text(
            "📩 للتواصل معنا:\nواتساب: ...\nتيليجرام: ...",
            reply_markup=InlineKeyboardMarkup(BACK_BUTTON)
        )

# ===== Error Handler =====
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Update {update} caused error {context.error}")

# ===== تشغيل البوت =====
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_error_handler(error_handler)

print("Bot is running...")
app.run_polling()
