import telebot
from config import token
from wikipars import get_cities

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nНапиши город)', parse_mode='html')

@bot.message_handler(commands=['Города'])
def list_city(message):
    print(get_cities())
    bot.send_message(message.chat.id, get_cities())


bot.polling(none_stop=True)
