from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re
import os
from aiohttp import web

# Configuration
TOKEN = os.getenv("TOKEN")  # Set in Render's environment variables
BOT_USERNAME = "@YourBotUsername"  # Replace with your bot's actual username

# Validate and calculate math expressions safely
def safe_eval(expression):
    if not re.match(r'^[\d\s+\-*/().,]+$', expression) or not any(op in expression for op in '+-*/()'):
        return None
    try:
        return eval(expression)
    except:
        return None

# Format numbers with commas (e.g., 1000 → 1,000)
def format_number(number):
    return f"{number:,}"

# Telegram handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔢 Send me a math problem like *2+2* or *(5*3)/2*!", parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text.startswith('/'):
        return
    
    result = safe_eval(text)
    if result is not None:
        await update.message.reply_text(f"✅ Result: `{format_number(result)}`", parse_mode="MarkdownV2")
    else:
        return  # Ignore invalid inputs

# Minimal HTTP server for Render compatibility
async def http_handler(request):
    return web.Response(text="Math Bot is running!")

async def run_server():
    app = web.Application()
    app.router.add_get('/', http_handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=int(os.getenv("PORT", 8080)))
    await site.start()

if __name__ == "__main__":
    # Start bot and HTTP server
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start_command))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    loop = bot_app.bot.get_updates_loop()
    loop.run_until_complete(run_server())
    bot_app.run_polling(allowed_updates=[])
