from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re
import os
from aiohttp import web

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable is missing or empty!")
print(f"Using token: {TOKEN}")
BOT_USERNAME = "@moonfkingbot"  # Replace with your bot's username

# Math evaluation logic
def safe_eval(expression):
    if not re.match(r'^(?=.*[+\-*/()])[\d\s+\-*/.()]+$', expression):
        return None
    try:
        return eval(expression)
    except:
        return None

def format_number(number):
    return f"{number:,}"

# Telegram bot handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me math expressions like 2+2 or (5*3)/2.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text.startswith('/'):
        return
    
    result = safe_eval(text)
    if result is not None:
        formatted_result = format_number(result)
        await update.message.reply_text(f"Result: {formatted_result}")
    else:
        return

# Minimal HTTP server to satisfy Render's port check
async def http_handler(request):
    return web.Response(text="Bot is running")

async def run_server():
    app = web.Application()
    app.router.add_get('/', http_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=int(os.getenv("PORT", 8080)))
    await site.start()

if __name__ == "__main__":
    # Start both the bot and HTTP server
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start_command))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    loop = bot_app.bot.get_updates_loop()
    loop.run_until_complete(run_server())
    bot_app.run_polling(allowed_updates=[])
