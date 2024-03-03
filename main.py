import json
from os import getenv
from typing import Final
from telegram import Bot
from telegram import Bot
from telegram import Update
from telegram.ext import Application , CommandHandler , MessageHandler , filters ,ContextTypes

from time import sleep # temp

from dotenv import load_dotenv
load_dotenv()

TOKEN:Final = getenv("apiToken")
telebot = Bot(TOKEN)

async def start_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    Username, password = update.message.text.replace("/start ", "").split(", ") #[rahul, 123]
    #print(Username , password)
    
    with open("database.json", "r+") as database:
        data = json.load(database)
        data[Username] = [password]
        json.dump(data, database, indent = 4)
 
async def imagine_command(update:Update, context: ContextTypes.DEFAULT_TYPE):
    userprompt = update.message.text[9:]
    print(userprompt)
    await update.message.reply_text('under_development')
    botreply = await telebot.send_message(chat_id=update.message.chat_id, text='loading.  ', reply_to_message_id=update.message.id)

    sleep(1)
    await telebot.edit_message_text(text="loading.. ", message_id=botreply.id, chat_id=botreply.chat_id)

    sleep(1)
    await telebot.edit_message_text(text="loading...", message_id=botreply.id, chat_id=botreply.chat_id)

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
    app.add_handler(CommandHandler('start',start_command))
    app.run_polling(poll_interval=3)

