from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json

from sheet_updater import start_update

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    interval_time = 1800    # 30 минут

    await update.message.reply_text(
        "👋 Discount alert включен!",
        parse_mode="HTML"
    )
    if not context.application.job_queue.jobs():
        context.application.job_queue.run_repeating(start_update_wrapper, interval=interval_time, first=0)

async def start_update_wrapper(context: ContextTypes.DEFAULT_TYPE):
    start_update()

def main():
    with open("credentials/tg.json", "r") as tg:
        tg_creds = json.load(tg)

    app = ApplicationBuilder().token(tg_creds["token"]).build()

    app.add_handler(CommandHandler("start", start))

    app.run_polling()

if __name__ == "__main__":
    main()