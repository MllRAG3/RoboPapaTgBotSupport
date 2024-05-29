from telebot.types import User, Message, InlineKeyboardMarkup, InlineKeyboardButton
from telebot.apihelper import ApiTelegramException
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

    def edit(self, **data):
        try:
            bot.edit_message_text(chat_id=self.message.chat.id, message_id=self.message.id, **data)
        except ApiTelegramException:
            bot.send_message(self.message.chat.id, bm.SOMETHING_WENT_WRONG)
            bot.edit_message_text(chat_id=self.message.chat.id, message_id=self.message.id + 1, **data)

    def start_greet(self):
        buttons = InlineKeyboardMarkup().add(InlineKeyboardButton('Оставить идею', callback_data='add_idea'))
        self.edit(text=bm.GREET, reply_markup=buttons)

    def add_idea(self):
        self.edit(text=bm.INPUT_IDEA)
        bot.register_next_step_handler(self.message, callback=self.register_idea)

    def register_idea(self, message: Message):
        bot.delete_message(message.chat.id, message.id)
        if len(message.text) > 1000:
            self.edit(text=bm.SOMETHING_WENT_WRONG)
            return

        data = {"user": self.db_user, "idea": message.text.strip()}
        UserIdeas.create(**data)
        buttons = InlineKeyboardMarkup().add(InlineKeyboardButton('Предложить еще идей', callback_data='add_idea'))
        self.edit(text=bm.THANKS_FOR_SUPPORTING, reply_markup=buttons)

    def all_ideas(self):
        if self.tb_user.id not in [1044385209]:
            buttons = InlineKeyboardMarkup().add(InlineKeyboardButton('Предложить идеи', callback_data='add_idea'))
            self.edit(text="На админке, сижу только я, а тебе нечего сюда тыкать", reply_markup=buttons)
            return
        for idea in UserIdeas.select():
            bot.send_message(self.message.chat.id, bm.IDEA.format(idea.id, idea.user.telegram_id, idea.idea), parse_mode='HTML')
            UserIdeas.delete_by_id(idea.id)
