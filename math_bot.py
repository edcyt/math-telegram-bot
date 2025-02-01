from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re

TOKEN = "7864983451:AAHU0caRv5k4CH9rpe5z9E-wcfMLDcLiaJk"  # Replace with your bot token
BOT_USERNAME = "@moonfkingbot"  # Replace with your bot's username

def safe_eval(expression):
    # Regex to allow numbers, spaces, +, -, *, /, ., and parentheses ()
    # Also enforce at least one operator or parenthesis
    if not re.match(r'^(?=.*[+\-*/()])[\d\s+\-*/.()]+$', expression):
        return None
    try:
        return eval(expression)
    except:
        return None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Send me a math problem like `(5+3)*2` or `10/(4-2)`.\n\n"
        "**Supported symbols**: `+`, `-`, `*`, `/`, `()`, and decimal numbers."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # Ignore messages starting with "/" (commands)
    if text.startswith('/'):
        return
    
    result = safe_eval(text)
    if result is not None:
        await update.message.reply_text(f"Result: `{result}`", parse_mode="MarkdownV2")
    else:
        # Don't reply at all if the input isn't a valid equation
        return

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling(allowed_updates=[])  # Add this parameter


