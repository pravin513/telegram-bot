from telegram.ext import ContextTypes

ADMIN_ID = 7306438851  # same admin id

async def broadcast(update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("❌ Use: /broadcast message")
        return

    users = context.application.bot_data.get("users", set())

    for uid in users:
        try:
            await context.bot.send_message(uid, text)
        except:
            pass

    await update.message.reply_text("📢 Broadcast sent")
