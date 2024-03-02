from typing import Final
from telegram import Update
from telegram.ext import Application , CommandHandler , MessageHandler , filters ,ContextTypes
TOKEN:Final='7039529223:AAEJjd_FlKhVf4yM8ChIKdYtWPEc390xpB4'
BOT_USERNAME:Final='@srisatb_bot'

async def prompt_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
    pass
    #await update.message.reply_text("I know that you don't have work?")

async def help_command(update:Update, context:ContextTypes.DEFAULT_TYPE):
      await update.message.reply_text("what the fuck wrong with you man!!!!!!")

async def custom_command( update:Update, context:ContextTypes.DEFAULT_TYPE):
       await update.message.reply_text("Please don't type I'm very busy!!okkkay!")

       #responses

def handle_response(text:str)->str:
   processed:str=text.lower()
   if 'hello ' in processed:
      return 'yeah tell!'
   if 'how are you' in processed:
       return'that is not your problem'
   if 'i love you' in processed:
      return'Dont act like a motherfucker'
   return ' i do not understand what you write? please do it correctly go the pee.....'

async def handle_message(update:Update, context: ContextTypes.DEFAULT_TYPE):
   message_type:str=update.message.chat.type
   text:str=update.message.text

   print(f'User({update.message.chat.id}) in {message_type}:"{text}"')

   if message_type=='group':
      if BOT_USERNAME in text:
         new_text:str=text.replace(BOT_USERNAME,'').strip()
         response:str=handle_response(new_text)
      else:
        return
   else:
      response:str=handle_response(text)  
   print('Bot:', response)
   await update.message.reply_text(response)

   async def error (update:Update, context: ContextTypes.DEFULT_type):
    print(f'Update{update}caused error{context.error}')

if __name__=='main':
     print('Starting bot....')
    app=Application.builder.token(TOKEN).build()
#commends
    
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('help',help_command))
    app.add_handler(CommandHandler('custom',custom_command))
         
#messages
    app.add_handler(MessageHandler(filters.TEXT,handle_message))
    #errors
    app.add_error_handler(error)
    #polls
    print('polling...')
    app.run_polling(poll_intetrval=3)
