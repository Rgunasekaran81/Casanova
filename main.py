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
    username = update.message.from_user.first_name
    if(update.message.from_user.last_name):
        username += " "+update.message.from_user.last_name
    return username
        
# read database
def read_database(filename:str) -> dict:
    data = {}
    with open(filename, "r") as database:
        data = json.load(database)
    return data 

# write database
def write_database(filename:str, data) -> None: 
    with open(filename, "w") as database:
        json.dump(data, database, indent = 4)

# to send message warning to user
async def sendmessage(update:Update, msg:str="", replaytomsg=True) -> None:
    await update.message.reply_text(msg, reply_to_message_id=update.message.message_id)

# root command functions
async def root_command(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command = update.message.text.replace("/root ", "").split()
 
    # command to initiate user
    if(command[0] == "init" and command[1] == "user"):
        if(len(command) == 2):
            sendmessage(update, "password missing, check /help init")
        elif(len(command) == 3):
            username = getusername(update)
            data = read_database("database.json")
            data[username] = {"password":command[2], "prompt":[]}
            data = read_database("database.json")
            data[username] = {"password":command[2], 
                              "chatid":update.message.chat.id, 
                              "logged in accounts":{getusername(update):update.message.chat.id}, 
                              "prompt":[]}
            write_database("database.json", data)

    #elif(command[0] == "login" ):
        
            
    # command to reset password
    elif(command[0] == "reset" and command[1] == "password"):
        if(len(command) == 4):
            data = read_database("database.json")
            username = getusername(update)
            if(command[2] == data[username]["password"]):
                data[username]["password"] = command[3]
                write_database("database.json", data)
        elif(len(command == 3)):
            pass
        else:
            sendmessage()
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
    userprompt = update.message.text.replace("/imagine ", "")
    data = read_database("database.json")
    userprompts = data[getusername(update)]["prompt"]
    if(len(userprompts) < 10):
        userprompts.append(userprompt)
    else:
        userprompts[0] = userprompt
    data[getusername(update)]["prompt"] = userprompts 
    write_database("database.json", data)
    with open("database.json", "r") as database:
            data = json.load(database)
           
            with open("database.json", "w") as database:
                json.dump(data, database, indent = 4)
            print(userprompt)    

    #await telebot.edit_message_text(text="loading...", message_id=botreply.id, chat_id=botreply.chat_id)

# help command function
async def help_command(update:Update,  context:ContextTypes.DEFAULT_TYPE) -> None:
    print(update.message.chat.id, update.message.chat_id)
    await sendmessage(update, """
    Casanova is a bot powered by Python to generate image
    List of commands:
        -> /root
        -> /imagine
    type '/help [command]' to get more details about the command
    """)

# run if main
if __name__=='__main__':
    app=Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("imagine", imagine_command))
    app.add_handler(CommandHandler("root", root_command))
    app.add_handler(CommandHandler("help", help_command))

    app.run_polling(poll_interval=2)