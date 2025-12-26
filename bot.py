from telegram.ext import ApplicationBuilder
from handlers import register_handlers

BOT_TOKEN = "8083967008:AAGGvBQhAkyi2asXy-nt6hawN9ftcY7n_ps"

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    register_handlers(app)
    app.run_polling()

if __name__ == "__main__":
    main()
