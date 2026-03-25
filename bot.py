from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os

# التوكن من Railway أو البيئة
TOKEN = os.getenv("TOKEN")

# ايديك
ADMIN_ID = 7228888995

# القائمة الرئيسية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 خدماتنا", callback_data='services')],
        [InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data='faq')],
        [InlineKeyboardButton("📩 إرسال استفسار", callback_data='ask')],
        [InlineKeyboardButton("🌐 زيارة الموقع", url='https://your-site.com')]
    ]
    await update.message.reply_text(
        "مرحباً بك في بوت تكنو درس 👨‍💻\nاختر من القائمة:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# الأزرار
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'services':
        await query.edit_message_text(
            "📚 خدماتنا:\n"
            "• حل الواجبات الجامعية\n"
            "• مشاريع التخرج\n"
            "• شروحات المواد\n\n"
            "📩 اختر (إرسال استفسار) للتواصل معنا"
        )

    elif query.data == 'faq':
        keyboard = [
            [InlineKeyboardButton("📩 كيف أرسل واجب؟", callback_data='q1')],
            [InlineKeyboardButton("💰 كم السعر؟", callback_data='q2')],
            [InlineKeyboardButton("⏱ وقت التسليم؟", callback_data='q3')],
            [InlineKeyboardButton("🔙 رجوع", callback_data='back')]
        ]
        await query.edit_message_text(
            "❓ اختر سؤالك:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == 'q1':
        await query.edit_message_text(
            "📩 يمكنك إرسال الواجب عبر البوت مباشرة\n"
            "أو التواصل معنا من خلال زر (إرسال استفسار)"
        )

    elif query.data == 'q2':
        await query.edit_message_text(
            "💰 السعر يعتمد على:\n"
            "• صعوبة الواجب\n"
            "• الوقت المطلوب\n"
            "• عدد الصفحات\n\n"
            "📩 راسلنا لمعرفة السعر بدقة"
        )

    elif query.data == 'q3':
        await query.edit_message_text(
            "⏱ مدة التسليم:\n"
            "من 24 ساعة إلى 72 ساعة حسب الطلب"
        )

    elif query.data == 'ask':
        context.user_data['waiting'] = True
        await query.edit_message_text("✍️ اكتب سؤالك الآن:")

    elif query.data == 'back':
        await start(update, context)

# استقبال الرسائل
async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting'):
        user = update.message.from_user
        text = update.message.text

        # ارسال لك
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 استفسار جديد:\n\n👤 {user.first_name}\n🆔 {user.id}\n\n📝 {text}"
        )

        await update.message.reply_text("✅ تم إرسال سؤالك، سيتم الرد عليك قريباً")

        context.user_data['waiting'] = False

# تشغيل البوت
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

print("Bot is running...")
app.run_polling()
