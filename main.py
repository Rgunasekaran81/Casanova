from os import getenv
from typing import Final
from telegram import Update
from telegram.ext import Application , CommandHandler , MessageHandler , filters ,ContextTypes

TOKEN:Final = getenv("apiToken")
   
   
async def imagine_command(update:Update,context: ContextTypes.DEFAULT_TYPE):
 await update.message.reply_text('under_development')





if __name__=='__main__':
 app=Application.builder().token(TOKEN).build()

 app.add_handler(CommandHandler('imagine',imagine_command))
 app.run_polling(poll_interval=3)
