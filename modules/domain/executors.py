from telebot.types import User, Message

from modules.constants.telegram_bot import bot
from modules.database.models.tg_users import TgUsers
from modules.database.models.user_ideas import UserIdeas


class Exec:
    def __init__(self, message: Message, user: User | None = None):
        self.message: Message = message
        self.tb_user: User = message.from_user if user is None else user

    def start_greet(self):
        pass
