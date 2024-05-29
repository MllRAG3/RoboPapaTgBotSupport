from modules.constants.telegram_bot import bot
from modules.domain.executors import Exec


@bot.message_handler(commands=['start'])
def start_message(message):
    pass


@bot.callback_query_handler(func=lambda call: call.data == 'add_idea')
def add_idea(call):
    pass


if __name__ == '__main__':
    print('Bot has been started!')
    bot.infinity_polling()
