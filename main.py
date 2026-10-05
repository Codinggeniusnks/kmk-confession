"""Private-message confession bot. Configure credentials outside the source code."""
import logging
import os
import threading
import time

from flask import Flask
from telegram import Update
from telegram.error import TelegramError
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Avoid HTTP request logging: Telegram API URLs contain the bot token.
logging.getLogger("httpx").setLevel(logging.CRITICAL)
logging.getLogger("httpcore").setLevel(logging.CRITICAL)
logging.getLogger("telegram").setLevel(logging.CRITICAL)
app = Flask(__name__)
PREFIX = "🫣 Anonymous Confession:\n"
COOLDOWN_SECONDS = 30


@app.route("/")
def home():
    return "KMK Confession Bot", 200


def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")), debug=False)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "💌 Welcome to KMK Confession! Send a text confession in this private chat.\n"
        "Only your text is published; this version does not forward your identity to admins.\n"
        "Telegram and the bot process your message and account information. "
        "Do not include names, contact details, or other identifying information.\n"
        "Keep posts respectful. Messages are published immediately, without moderation."
    )


async def confess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if message is None or update.effective_chat is None or update.effective_chat.type != "private":
        return
    text = (message.text or "").strip()
    if not text or len((PREFIX + text).encode("utf-16-le")) // 2 > 4000:
        await message.reply_text("Please send a shorter text confession (under 4,000 characters).")
        return
    now = time.monotonic()
    last = context.user_data.get("last_confession_at")
    if last is not None and now - last < COOLDOWN_SECONDS:
        await message.reply_text("Please wait 30 seconds between confessions.")
        return
    try:
        await context.bot.send_message(chat_id=context.bot_data["confession_channel"], text=PREFIX + text)
    except TelegramError:
        await message.reply_text("Unable to publish right now. Please try again later.")
        return
    context.user_data["last_confession_at"] = now
    await message.reply_text("✅ Your confession was published without your Telegram name or ID.")


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE):
    # Never log the update, exception, sender, confession, or token-bearing URLs.
    logging.getLogger(__name__).error("Bot request failed; private details omitted.")


def main():
    token = os.environ.get("BOT_TOKEN", "").strip()
    channel = os.environ.get("CONFESSION_CHANNEL", "").strip()
    if not token or not channel:
        raise SystemExit("Set BOT_TOKEN and CONFESSION_CHANNEL in your hosting environment.")
    application = ApplicationBuilder().token(token).build()
    application.bot_data["confession_channel"] = channel
    application.add_handler(CommandHandler("start", start, filters=filters.ChatType.PRIVATE))
    application.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, confess))
    application.add_error_handler(on_error)
    threading.Thread(target=run_flask, daemon=True).start()
    application.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
