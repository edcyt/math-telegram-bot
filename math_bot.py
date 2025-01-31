from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re

# Replace 'YOUR_TOKEN' with your bot's API token
TOKEN = "7864983451:AAF3WKVbfkcNjYNU01oCLXBk5sNZpkXzeus"
BOT_USERNAME = "@moonfkingbot"  # e.g., @MathHelperBot

# Validate input to prevent code injection
def safe_eval(expression):
    # Allow only numbers, spaces, and + - * / .
    if not re.match(r'^[\d\s+\-*/.]+$', expression):
        return None
    try:
        return eval(expression)
    except:
        return None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me a math problem like '5+3' or '4*2'.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith('/'):
        return  # Ignore other commands

    result = safe_eval(text)
    if result is not None:
        await update.message.reply_text(f"Result: {result}")
    else:
        await update.message.reply_text("❌ Invalid input. Use numbers and + - * / only.")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()