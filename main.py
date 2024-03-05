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
    
    # actual command execution
    elif(command[0] == "init"):
        if(len(command) == 1):
            await sendmessage(update, "init requires atleast 1 argument (user) \ntype '/help root' to see more options")
        elif(command[1] == "user"):
            if(len(command) == 2): # [init, user] display error when no password given
                await sendmessage(update, "init user requires 1 argument <password> \ntype '/help root' to see more options") 
            elif(len(command) == 3):
                if(len(command[2]) < 8 or not command[2].isalnum() or len(command[2]) > 15):
                    await sendmessage(update, "password should be minimum 8 characters maximum 15 characters with mixture of alphfabets and numbers")
                    return 
                username = getusername(update)
                data = read_database("database.json")
                data[username] = {"password":command[2],
                              "current_login":getusername(update),
                              "chatid":update.message.chat.id,
                              "logged in accounts":{getusername(update):update.message.chat.id},
                              "prompt":[]}
                write_database("database.json", data)
                await sendmessage(update, f"User initialized. \nUsername: {username}")

    elif(command[0] == "login"):
        if(len(command) < 3):
            await sendmessage(update, "login requires 2 arguments <username> <password> \ntype '/help root' to see more options")
        else:
            data = read_database("database.json")
            if(command[1] in data):
                if(data[command[1]]["password"] == command[2]):
                    data[command[1]]["logged in accounts"][getusername(update)] = update.message.chat.id
                    data[getusername(update)]["current_login"] = command[1]
                    write_database("database.json", data)
                    await sendmessage(update, f"Successfully logged in as {command[1]}")
                else:
                    await sendmessage(update, "Wrong password")
            else:
                await sendmessage(update, "User not found in database")

    # command to reset password
    elif(command[0] == "reset"):
        if(len(command) == 1):
            await sendmessage(update, "reset requires atleast 1 arguments \ntype '/help root' to see more options")
        elif(command[1] == "password"):
            if(len(command) < 3):
                await sendmessage(update, "reset password requires atleast 1 arguments '[old password] <new password>' \ntype '/help root' to see more options")
            elif(len(command) == 4):
                data = read_database("database.json")
                username = getusername(update)
                if(command[2] == data[username]["password"]):
                    if(len(command[3]) < 8 or not command[3].isalnum() or len(command[3]) > 15):
                        await sendmessage("password should be minimum 8 characters maximum 15 characters with mixture of alphfabets and numbers")
                        return 
                    data[username]["password"] = command[3]
                    write_database("database.json", data)
                    await sendmessage(update, "Password changed successfully")
                else:
                    await sendmessage(update, "Old password didn't match")
            elif(len(command == 3)):
                if(len(command[2]) < 8 or not command[2].isalnum() or len(command[2]) > 15):
                    await sendmessage("password should be minimum 8 characters maximum 15 characters with mixture of alphfabets and numbers")
                    return 

    # command to show/delete prompts from databse
    elif(command[0] == "prompt"):
        if(len(command) < 2):
            await sendmessage(update, "prompt requires 1 argument 'show/delete' \ntype '/help root' to see more options")
        elif(command[1] == "show"):
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
    command = update.message.text("/help ", "").split() # /help root; command = [root]
    
    if(command[0] == "/help"):
        await sendmessage(update, """
        Casanova is a bot powered by Python to generate image
        List of commands:
            -> /root - To manage account data, available arguments [init, login, prompt, reset, user].
            -> /imagine -> To generate image.
        type '/help [command]' to get more details about the command.
        """)
    # /help root
    elif(command[0] == "root"):
        await sendmessage(update, """
        Root command gives you access and manage user data.
        List of root commands:
            -> init (user) <password> - To initalize a new user.
            -> login <username> <password> - To login into a account.
            -> prompt (show, delete) [number] - 
            -> reset (password) [old password] <new password> - 
        """)

    # /help imagine
    elif(command[0] == "imagine"):
        await sendmessage(update, """ 
        Imagine command in casanova_bot help's bots to generaye image.
        Imagin command requires 1 argument that is user  prompt""")

# run if main
if __name__=='__main__':
    app=Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("imagine", imagine_command))
    app.add_handler(CommandHandler("root", root_command))
    app.add_handler(CommandHandler("help", help_command))

    app.run_polling(poll_interval=2)