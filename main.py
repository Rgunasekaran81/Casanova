from casanova_util import *
from os import getenv
from typing import Final
from telegram import Update
#from telegram import Bot
from telegram.ext import Application , CommandHandler , MessageHandler , filters ,ContextTypes
from dotenv import load_dotenv
load_dotenv()

from time import sleep # temp

TOKEN:Final = getenv("apiToken")
#telebot = Bot(TOKEN)

# root command functions
async def root_command(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command = update.message.text.replace("/root ", "").split()
    
    """
    /root  (no argument) -> 27
    /root login (with one/no argument) -> 32
    /root prompt (with no argument) -> 38
    /root reset password(with no argument) -> 
    /root (with invalid argument) -> 97
    """

    # warning for wrong command '/root'
    if(command[0] == "/root"):
        await sendmessage(update, "no argument given \ntype '/help root' to see more options")

    # actuall command for login '/root login <username> <password>
    # warning for wrong command '/root login <username>'
    elif (command[0] == "login" and len(command) < 3):
        await sendmessage(update, "login requires two arguments username and password \ntype '/help root' to see more options")

    # actuall command for prompt '/root prompt show/delete [num]
    # warning for invalid prompt command
    elif():
        pass
    
    # actual command for reset password '/root reset password [old password] <newpassword>
    # warning for invalid reset password
    elif():
        pass

    # actual command execution
    elif(command[0] == "init" and command[1] == "user"):
        if(len(command) == 2): # [init, user] display error when no password given
            await sendmessage(update, "password missing, check /help init") 
        elif(len(command) == 3):
            username = getusername(update)
            data = read_database("database.json")
            data[username] = {"password":command[2], "prompt":[]}
            data = read_database("database.json")
            data[username] = {"password":command[2],
                              "current_login":getusername(update),
                              "chatid":update.message.chat.id,
                              "logged in accounts":{getusername(update):update.message.chat.id},
                              "prompt":[]}
            write_database("database.json", data)

    elif(command[0] == "login"):
        data = read_database("database.json")
        if(command[1] in data):
            if(data[command[1]]["password"] == command[2]):
                data[command[1]]["logged in accounts"][getusername(update)] = update.message.chat.id
                data[getusername(update)]["current_login"] = command[1]
                write_database("database.json", data)
            else:
                pass
        else:
            pass

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
    elif(command[0] == "prompt"):
        if(command[1] == "show"):
            data = read_database("database.json")
            current_login = data[getusername(update)]["current_login"]
            prompts = data[current_login]["prompt"]
            displayprompt = ""
            for i in range(len(prompts)):
                displayprompt += prompts[i]+"\n"
            await sendmessage(update, displayprompt)

        elif(command[1] == "delete"):
            pass

    # command to delete userdata
    elif(command[0] == "delete" and command[1] == "userdata"):
        pass

    # warning for wrong command '/root'
    else: 
        await sendmessage(update, f"{update.message.text} is not recognized as a command \ntype '/help root' to see more options")

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