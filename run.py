import telebot
from config import token
from wikipars import get_cities

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nНапиши /Города\n'
                                      f'Или пиши название города, я тебе помогу! ^_^', parse_mode='html')


@bot.message_handler(commands=['Города'])
def list_city(message):
    answer = ''
    for city in get_cities():
        answer += city + '\n'

    bot.send_message(message.chat.id, answer)


@bot.message_handler(func=lambda m: True)
def reply(message):
    answer = ''
    for city in get_cities():
        if city.startswith(message.text):
            answer += city + '\n'
    if answer:
        bot.send_message(message.chat.id, answer)
    else:
        bot.send_message(message.chat.id, 'Городов с таким названием нет в базе, попробуйте ещё раз! :(')


if __name__ == '__main__':
    bot.polling(none_stop=True)
