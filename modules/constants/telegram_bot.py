from config import BOT_TOKEN
from telebot import TeleBot
from typing import Final

bot: Final[TeleBot] = TeleBot(BOT_TOKEN)
