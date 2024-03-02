from os import getenv
from typing import Final
import telegram
from telegram.ext import Application , CommandHandler , MessageHandler , filters ,ContextTypes

TOKEN:Final = getenv("apiToken")

