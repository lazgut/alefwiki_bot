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
    count = 0
    dict_city = get_cities()
    for city in dict_city.keys():
        if city.startswith(message.text):
            answer += city + '\n'
            count += 1
    if count > 1:
        bot.send_message(message.chat.id, f'Назовите город более точно, вот ваши варианты:\n{answer}')
    elif count == 1:
        bot.send_message(message.chat.id, f'Город который вы ищите - {answer}\n'
                                          f'Ссылка на город - https://ru.wikipedia.org{dict_city[answer[:-1]]}')
    else:
        bot.send_message(message.chat.id, 'Городов с таким названием нет в базе, попробуйте ещё раз! :(')


if __name__ == '__main__':
    bot.polling(none_stop=True)
