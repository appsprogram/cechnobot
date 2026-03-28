# bot.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

# ===== إعدادات البوت =====
TOKEN = os.getenv("TOKEN")

# رابط GitHub للصور فقط
GITHUB_RAW = "https://raw.githubusercontent.com/appsprogram/cechnobot/main/media/"

# رابط الفيديو (Catbox)
ALEKS_VIDEO_URL = "https://files.catbox.moe/a9l29d.mp4"

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

# ===== الصور فقط =====
MEDIA_FILES = [
    "ALEKS1.jpg",
    "other1.jpg",
    "help1.jpg",
    "help2.jpg",
    "help3.png"
]

# ===== البداية =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً بك في بوت تكنو درس 👨‍💻\n"
        "بوت مساعد حول الاستفسارات...\n\n"
        "اختر من القائمة:",
        reply_markup=InlineKeyboardMarkup(MAIN_MENU)
    )

# ===== إرسال صور من GitHub =====
async def send_images_by_prefix(context, chat_id, prefix):
    for f in MEDIA_FILES:
        if f.lower().startswith(prefix.lower()):
            url = GITHUB_RAW + f
            await context.bot.send_photo(chat_id=chat_id, photo=url)

# ===== الأزرار =====
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat.id

    # الرئيسية
    if data == "home":
        await query.edit_message_text(
            "القائمة الرئيسية:",
            reply_markup=InlineKeyboardMarkup(MAIN_MENU)
        )

    # عرض الإجابات
    elif data == "answers":
        await context.bot.send_message(chat_id=chat_id, text="📊 عرض إجابتنا للطلاب")
        await query.edit_message_text(
            "اختر:",
            reply_markup=InlineKeyboardMarkup(ANSWERS_MENU)
        )

    # ALEKS
    elif data == "aleks":
        await context.bot.send_message(chat_id=chat_id, text="📊 الإحصاء - ALEKS")

        # إرسال الصور
        await send_images_by_prefix(context, chat_id, "ALEKS")

        # إرسال الفيديو من Catbox
        await context.bot.send_video(
            chat_id=chat_id,
            video=ALEKS_VIDEO_URL,
            caption="🎥 شرح ALEKS"
        )

    # واجبات أخرى
    elif data == "other":
        await context.bot.send_message(chat_id=chat_id, text="📚 واجبات أخرى")
        await send_images_by_prefix(context, chat_id, "other")

    # كيفية الاشتراك
    elif data == "alek_help":
        await context.bot.send_message(chat_id=chat_id, text="📘 كيفية الاشتراك بمنصة ALEKS")

        await context.bot.send_photo(
            chat_id=chat_id,
            photo=GITHUB_RAW + "help1.jpg",
            caption="هل عندك تطبيق التحقق المربوط بالبلاك بورد؟"
        )

        keyboard = [
            [InlineKeyboardButton("📱 iPhone", url="https://apps.apple.com")],
            [InlineKeyboardButton("🤖 Android", url="https://play.google.com")]
        ]

        await context.bot.send_message(
            chat_id=chat_id,
            text="تحميل تطبيق KAU Authenticator:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        await context.bot.send_message(
            chat_id=chat_id,
            text="إذا لم تربط التطبيق بعد:\nتواصل مع الدعم:\n+966126952209"
        )

        for img in ["help2.jpg", "help3.png"]:
            await context.bot.send_photo(chat_id=chat_id, photo=GITHUB_RAW + img)

        await context.bot.send_message(
            chat_id=chat_id,
            text="🔙 للرجوع:",
            reply_markup=InlineKeyboardMarkup(BACK_BUTTON)
        )

    # التواصل
    elif data == "contact":
        await context.bot.send_message(chat_id=chat_id, text="📩 التواصل معنا")
        await query.edit_message_text(
            "📩 واتساب: ...\n📱 تيليجرام: ...",
            reply_markup=InlineKeyboardMarkup(BACK_BUTTON)
        )

# ===== التشغيل =====
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot is running...")
app.run_polling()
