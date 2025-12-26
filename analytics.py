from telegram import Update
from telegram.ext import ContextTypes
from database import top_products

ADMIN_ID = 7306438851

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    rows = top_products()

    if not rows:
        await update.message.reply_text("No data yet")
        return

    msg = "📊 Top Searched Products\n\n"
    for name, count in rows:
        msg += f"{name} – {count} searches\n"

    await update.message.reply_text(msg)
