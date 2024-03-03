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

async def showwarning(update:Update, string:str="") -> None:
    pass

async def root_command(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command = update.message.text.replace("/root ", "").split()

    # going to change the login/register username, password system. 
    if(command[0] == "login"):
        if(len(command) == 1):
            await telebot.send_message(chat_id=update.message.chat_id, text="type '/root login <username> <password>' to login", reply_to_message_id=update.message.id)
        elif(len(command) == 3):
            Username, password = command[1], command[2]
            data = {}
            with open("database.json", "r") as database:
                data = json.load(database)
                if(data[Username] != [password]):
                    showwarning("password does not match")
                    return
                # add user as logged in device
        else:
            showwarning()
    
    elif(command[0] == "register"):
        if(len(command) == 1):
            await telebot.send_message(chat_id=update.message.chat_id, text="type '/root register <username> <password>' to login", reply_to_message_id=update.message.id)
        elif(len(command) == 3):
            username, password = command[1], command[2]
            data = {}
            with open("database.json", "r") as database:
                data = json.load(database)
                if(username in data):
                    showwarning("User already exist")
                    return
                data[username] = [password]
            with open("database.json", "w") as database:
                json.dump(data, database, indent = 4)
        else:
            showwarning()

    elif(command == "show prompt"):
        pass
    elif(command == "delete prompt"):
        pass
    elif(command == "delete user"):
        pass
   
async def imagine_command(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userprompt = update.message.text[9:]
    print(userprompt)
    botreply = await telebot.send_message(chat_id=update.message.chat_id, text='loading.  ', reply_to_message_id=update.message.id)

    sleep(1)
    await telebot.edit_message_text(text="loading.. ", message_id=botreply.id, chat_id=botreply.chat_id)

    sleep(1)
    await telebot.edit_message_text(text="loading...", message_id=botreply.id, chat_id=botreply.chat_id)

async def help_command(update:Update,  context:ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("""
    Hello i'm Casanova, Telegram bot to generate image based on prompt
    Available commands:
        /help
        /imagine [prompt] (under development)   
                                    """)


if __name__=='__main__':
    app=Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('imagine',imagine_command))
    app.add_handler(CommandHandler('root',root_command))
    app.run_polling(poll_interval=3)

