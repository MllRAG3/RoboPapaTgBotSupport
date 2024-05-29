from telebot.types import User, Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime

from modules.constants.telegram_bot import bot
import modules.constants.bot_messages as bm
from modules.database.models.tg_users import TgUsers
from modules.database.models.user_ideas import UserIdeas


class Exec:
    def __init__(self, message: Message, user: User | None = None):
        self.message: Message = message
        self.tb_user: User = message.from_user if user is None else user
        self.db_user: TgUsers = TgUsers.get_or_create(telegram_id=self.tb_user.id, chat_id=message.chat.id)[0]
        self.db_user.last_update = datetime.now()
        TgUsers.save(self.db_user)

    def start_greet(self):
        buttons = InlineKeyboardMarkup().add(InlineKeyboardButton('Оставить идею', callback_data='add_idea'))
        bot.send_message(self.message.chat.id, bm.GREET, reply_markup=buttons)

    def add_idea(self):
        bot.send_message(self.message.chat.id, bm.INPUT_IDEA)
        bot.register_next_step_handler(self.message, callback=self.register_idea)

    def register_idea(self, message: Message):
        if len(message.text) > 1000:
            bot.send_message(self.message.chat.id, bm.SOMETHING_WENT_WRONG)
            return

        data = {"user": self.db_user, "idea": message.text.strip()}
        UserIdeas.create(**data)
        buttons = InlineKeyboardMarkup().add(InlineKeyboardButton('Предложить еще идей', callback_data='add_idea'))
        bot.send_message(self.message.chat.id, bm.THANKS_FOR_SUPPORTING, reply_markup=buttons)
