from os import getenv
from typing import Final
from telegram import Update
from telegram.ext import Application , CommandHandler , MessageHandler , filters ,ContextTypes

TOKEN:Final = getenv("apiToken")
   
   
async def imagine_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    userprompt = update.message.text[9:]
    print(userprompt)
    await update.message.reply_text('under_development')

async def help_command(update:Update,  context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
    Hello i'm Casanova, Telegram bot to generate image based on prompt
    Available commands:
        /help
        /imagine [prompt] (under development)   
                                    """)

if __name__=='__main__':
    app=Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('imagine',imagine_command))
    app.run_polling(poll_interval=3)