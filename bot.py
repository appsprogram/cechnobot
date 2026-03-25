from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = 7228888995

# ===== القوائم =====

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 خدماتنا", callback_data='services')],
        [InlineKeyboardButton("❓ الأسئلة الشائعة", callback_data='faq')],
        [InlineKeyboardButton("📩 إرسال استفسار", callback_data='ask')],
        [InlineKeyboardButton("🌐 زيارة الموقع", url='https://your-site.com')]
    ])

def back_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 رجوع", callback_data='home')]
    ])

# ===== البداية =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 مرحباً بك في بوت تكنو درس الذكي\nاختر من القائمة:",
        reply_markup=main_menu()
    )

# ===== الأزرار =====

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # الرئيسية
    if data == "home":
        await query.edit_message_text(
            "👋 القائمة الرئيسية:",
            reply_markup=main_menu()
        )

    # الخدمات
    elif data == "services":
        await query.edit_message_text(
            "📚 خدماتنا:\n\n"
            "• حل الواجبات الجامعية\n"
            "• مشاريع التخرج\n"
            "• شروحات المواد\n\n"
            "📩 تواصل معنا لطلب الخدمة",
            reply_markup=back_button()
        )

    # FAQ
    elif data == "faq":
        keyboard = [
            [InlineKeyboardButton("📩 كيف أرسل واجب؟", callback_data='q1')],
            [InlineKeyboardButton("💰 كم السعر؟", callback_data='q2')],
            [InlineKeyboardButton("⏱ وقت التسليم؟", callback_data='q3')],
            [InlineKeyboardButton("🔙 رجوع", callback_data='home')]
        ]
        await query.edit_message_text(
            "❓ اختر سؤالك:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "q1":
        await query.edit_message_text(
            "📩 أرسل الواجب مباشرة عبر البوت\nوسيتم الرد عليك",
            reply_markup=back_button()
        )

    elif data == "q2":
        await query.edit_message_text(
            "💰 السعر يعتمد على صعوبة الواجب\n📩 راسلنا للتفاصيل",
            reply_markup=back_button()
        )

    elif data == "q3":
        await query.edit_message_text(
            "⏱ التسليم خلال 24 - 72 ساعة",
            reply_markup=back_button()
        )

    # ارسال استفسار
    elif data == "ask":
        context.user_data['waiting'] = True
        await query.edit_message_text(
            "✍️ اكتب سؤالك الآن:",
            reply_markup=back_button()
        )

# ===== الرسائل =====

async def messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting'):
        user = update.message.from_user
        text = update.message.text

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 استفسار جديد\n\n👤 {user.first_name}\n🆔 {user.id}\n\n📝 {text}"
        )

        await update.message.reply_text("✅ تم إرسال سؤالك")
        context.user_data['waiting'] = False

# ===== التشغيل =====

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, messages))

print("Bot is running...")
app.run_polling()
