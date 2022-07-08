import telebot
from config import token, host, port, user, password, db_name
from wikipars import get_cities

import pandas as pd
import psycopg2
from sqlalchemy import create_engine

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nНапиши /Города\n'
                                      f'Или пиши название города, я тебе помогу! ^_^')


@bot.message_handler(commands=['Города'])
def list_city(message):
    answer = ''
    for city in get_cities():
        answer += city + '\n'

    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=['update'])
def update_db(message):
    df_values = pd.DataFrame.from_dict(get_cities(), orient='index', columns=['Численность', 'Раздел вики'])
    print(df_values)
    dataframe_to_postgresql(df_values)


@bot.message_handler(func=lambda m: True)  # Обрабатывает сообщения с частичным/полным названием города
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
                                          f'Численность города - {dict_city[answer[:-1]][0]}\n'
                                          f'Ссылка на город - https://ru.wikipedia.org{dict_city[answer[:-1]][1]}')
    else:
        bot.send_message(message.chat.id, 'Городов с таким названием нет в базе, попробуйте ещё раз! :(')


def dataframe_to_postgresql(df_values):  # Записываем DataFrame в таблицу postgresql с обратной связью по postgresql
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )

            print(f"Server version: {cursor.fetchone()}")

        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
        df_values.to_sql('alefwikibot', con=engine, if_exists='replace', index=True, index_label='Город'), engine.execute(f"SELECT * FROM alefwikibot").fetchall()

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            connection.close()

            print("[INFO] PostgreSQL connection closed")


if __name__ == '__main__':
    bot.polling(none_stop=True)
