from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from database import init_db, search_products
from admin import addproduct, admin_photo
from broadcast import broadcast
from analytics import stats

BOT_TOKEN = "8083967008:AAGGvBQhAkyi2asXy-nt6hawN9ftcY7n_ps"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = context.application.bot_data.setdefault("users", set())
    users.add(update.message.from_user.id)

    await update.message.reply_text(
        "🙏 Welcome to Smart Product Shop Bot\n\n"
        "🔍 Product का नाम लिखो\n"
        "Example: saree, keyboard, mouse"
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = context.application.bot_data.setdefault("users", set())
    users.add(update.message.from_user.id)

    text = update.message.text.lower()
    results = search_products(text)

    if not results:
        await update.message.reply_text("❌ Product नहीं मिला")
        return

    for _, name, price, link, photo in results:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🛒 Buy Now", url=link)]
        ])

        if photo:
            await update.message.reply_photo(
                photo=photo,
                caption=f"🛒 {name}\n💰 {price}",
                reply_markup=keyboard
            )
        else:
            await update.message.reply_text(
                f"🛒 {name}\n💰 {price}\n🔗 {link}",
                reply_markup=keyboard
            )

def main():
    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addproduct", addproduct))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.PHOTO, admin_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()
