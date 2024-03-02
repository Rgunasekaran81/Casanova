from os import getenv
from typing import Final
from telegram import Update
from telegram.ext import Application , CommandHandler , MessageHandler , filters ,ContextTypes

TOKEN:Final = getenv("apiToken")


async def help_command(update:Update,  context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
    Hello i'm Casanova, Telegram bot to generate image based on prompt
    Available commands:
        /help
        /imagine [prompt] (under development)   
                                    """)

app=Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler('help',help_command))
app.run_polling(poll_interval=3)