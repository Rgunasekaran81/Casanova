import json
from telegram import Update

def getusername(update:Update) -> str:
    """
    Gets the first name and last name of the user from the Update object.

    Args:
        update (Update): An object representing the update received from the user.
    Returns:
        str: First name and Last name of the user without whitespace.
    """
    username = update.message.from_user.first_name
    if(update.message.from_user.last_name):
        username += update.message.from_user.last_name
    return username
        
def read_database(filename:str) -> dict:
    """
    Read the provoided json file.

    Args:
        filename (str): Json file to be read.

    Returns:
        dict: Data from the provoided json file
    """
    data = {}
    with open(filename, "r") as database:
        data = json.load(database)
    return data 

def write_database(filename:str, data:dict) -> None: 
    """
    Write into the provoided json file

    Args:
        filename (str): Json file to writen
        data (dict): Data to be entered
    """
    with open(filename, "w") as database:
        json.dump(data, database, indent = 4)

async def sendmessage(update:Update, msg:str, replytomsg=True) -> Update:
    """
    Sends a message to the provided Update object

    Args:
        update (Update): An object representing the update received from the user.
        msg (str): The message to be sent.
        replytomsg (bool, optional): A flag indicating wheter to send the message by tagging the message from update. Defaults to True

    Returns:
        Update: Update object of the message sent by the bot.  
    """
    return await update.message.reply_text(msg, reply_to_message_id=update.message.message_id)