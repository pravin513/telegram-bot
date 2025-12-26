from telegram import Update
from telegram.ext import ContextTypes
from database import add_product

ADMIN_ID = 7306438851  # 👈 अपना Telegram ID यहाँ डालो

async def addproduct(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    try:
        data = " ".join(context.args)
        name, keywords, price, link = data.split("|")

        context.user_data["pending_product"] = {
            "name": name.strip(),
            "keywords": keywords.strip().lower(),
            "price": price.strip(),
            "link": link.strip()
        }

        await update.message.reply_text("📸 अब product की PHOTO भेजो")

    except:
        await update.message.reply_text(
            "❌ Format:\n/addproduct Name | keywords | price | link"
        )

async def admin_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    if "pending_product" not in context.user_data:
        return

    photo_id = update.message.photo[-1].file_id
    p = context.user_data.pop("pending_product")

    add_product(
        p["name"],
        p["keywords"],
        p["price"],
        p["link"],
        photo_id
    )

    await update.message.reply_text("✅ Product added with photo")
