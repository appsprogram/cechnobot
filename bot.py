from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 7228888995

# رابط GitHub raw (غيره حسب حسابك)
GITHUB_RAW = "https://raw.githubusercontent.com/USERNAME/REPO/main/media/"

# ===== القوائم =====

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 عرض إجابتنا للطلاب", callback_data='answers')],
        [InlineKeyboardButton("📘 كيفية الاشتراك بمنصة ALEKS", callback_data='alek_help')],
        [InlineKeyboardButton("📩 التواصل معنا", callback_data='contact')]
    ])

def back():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 رجوع", callback_data='home')]
    ])

# ===== البداية =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً بك في بوت تكنو درس 👨‍💻\n"
        "بوت مساعد حول الاستفسارات...\n\n"
        "اختر من القائمة:",
        reply_markup=main_menu()
    )

# ===== إرسال ملفات من GitHub =====

async def send_media_by_prefix(context, chat_id, prefix):
    files = [
        "ALEKS1.jpg",
        "ALEKS_video.mp4",
        "other1.jpg"
    ]

    for f in files:
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

    # الرئيسية
    if data == "home":
        await query.edit_message_text(
            "القائمة الرئيسية:",
            reply_markup=main_menu()
        )

    # عرض الإجابات
    elif data == "answers":
        keyboard = [
            [InlineKeyboardButton("📊 الإحصاء - ALEKS", callback_data='aleks')],
            [InlineKeyboardButton("📚 واجبات أخرى", callback_data='other')],
            [InlineKeyboardButton("🔙 رجوع", callback_data='home')]
        ]
        await query.edit_message_text("اختر:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data == "aleks":
        await send_media_by_prefix(context, query.message.chat_id, "aleks")

    elif data == "other":
        await send_media_by_prefix(context, query.message.chat_id, "other")

    # شرح ALEKS
    elif data == "alek_help":

        # 1
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=GITHUB_RAW + "help1.png",
            caption="هل عندك تطبيق التحقق؟"
        )

        # 2
        keyboard = [
            [InlineKeyboardButton("📱 تحميل iPhone", url="https://apps.apple.com")],
            [InlineKeyboardButton("🤖 تحميل Android", url="https://play.google.com")]
        ]
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="تحميل تطبيق KAU Authenticator:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        # 3
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="إذا لم تربط التطبيق:\n"
                 "تواصل مع الدعم:\n"
                 "+966126952209"
        )

        # 4
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=GITHUB_RAW + "help2.png"
        )

        # 5
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=GITHUB_RAW + "help3.png"
        )

        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="🔙 للرجوع للقائمة استخدم الزر",
            reply_markup=back()
        )

    # تواصل
    elif data == "contact":
        await query.edit_message_text(
            "📩 للتواصل معنا:\n"
            "واتساب: ...\n"
            "تيليجرام: ...",
            reply_markup=back()
        )

# ===== التشغيل =====

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

print("Bot is running...")
app.run_polling()
