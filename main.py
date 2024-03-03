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

# returns username
def getusername(update:Update, split="") -> str:
    return update.message.from_user.first_name+split+update.message.from_user.last_name

# to send message warning to user
async def showwarning(update:Update, string:str="") -> None:
    pass

# root command functions 
async def root_command(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command = update.message.text.replace("/root ", "").split()
 
    # command to initiate user
    if(command[0] == "init" and command[1] == "user"):
        if(len(command) == 2):
            showwarning()
        elif(len(command) == 3):
            username = getusername(update)
            with open("database.json", "r") as database:
                data = json.load(database)
                data[username] = {"password":command[2], "prompt":[]}
                with open("database.json", "w") as database:
                    json.dump(data, database, indent = 4)
    # command to reset password
    elif(command[0] == "reset" and command[1] == "password"):
        if(len(command) == 4):
            with open("database.json", "r") as database:
                    data = json.load(database)
                    username = getusername(update) 
                    if(command[2] == data[username]["password"]):
                        data[username]["password"] = command[3]
                        with open("database.json", "w") as database:
                            json.dump(data, database, indent = 4)
        elif(len(command == 3)):
            pass
        else:
            showwarning()
    # command to show/delete prompts from databse
    elif(command[1] == "prompt"):
        with open("database.json", "r") as database:
                data = json.load(database)
                if(command[0] == "show"):
                #    prompt = data[telebot.]
                 #   await telebot.send_message(chat_id=update.message.chat_id, text=, reply_to_message_id=update.message.id)
                    pass
                elif(command[1] == "delete"):
                    pass
    # command to delete userdata
    elif(command[0] == "delete" and command[1] == "userdata"):
        pass

# imagine command to get prompt and send image
async def imagine_command(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    userprompt = update.message.text[9:]
    with open("database.json", "r") as database:
            data = json.load(database)
            userprompts = data[getusername(update)]["prompt"]
            if(len(userprompts) < 10):
                userprompts.append(userprompt)
            else:
                userprompts[0] = userprompt
            data[getusername(update)]["prompt"] = userprompts 
            with open("database.json", "w") as database:
                json.dump(data, database, indent = 4)
            print(userprompt)    

    botreply = await telebot.send_message(chat_id=update.message.chat_id, text='loading.  ', reply_to_message_id=update.message.id)

    sleep(1)
    await telebot.edit_message_text(text="loading.. ", message_id=botreply.id, chat_id=botreply.chat_id)

    sleep(1)
    await telebot.edit_message_text(text="loading...", message_id=botreply.id, chat_id=botreply.chat_id)

# help command function
async def help_command(update:Update,  context:ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("""
    Hello i'm Casanova, Telegram bot to generate image based on prompt
    Available commands:
        /help
        /imagine [prompt] (under development)   
                                    """)
# run if main
if __name__=='__main__':
    app=Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('imagine',imagine_command))
    app.add_handler(CommandHandler('root',root_command))
    app.run_polling(poll_interval=2)