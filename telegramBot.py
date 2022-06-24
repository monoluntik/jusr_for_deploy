import logging
import sqlite3

import telebot
from telebot import types
from basketballDriver import BasketballBet
from time import sleep
import threading

dp = telebot.TeleBot('5495120334:AAHTrgJRvWcQb4am477CTdLA1aVeGFhg9_o')

logging.basicConfig(level=logging.INFO)

users_list = dict()

DELAY = 60


db = sqlite3.connect("botUsers.db", check_same_thread=False)
sqlite_create_table_query = """CREATE TABLE IF NOT EXISTS users(
                            id TEXT);"""

sql = db.cursor()
sql.execute(sqlite_create_table_query)
db.commit()


@dp.message_handler(commands=["start"])
def start(message: types.Message):
    user_id = message.chat.id
    sql.execute(f"SELECT id FROM users WHERE id = {user_id}")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?)", (user_id,),)
        db.commit()
    users = sql.execute(f"SELECT * FROM users").fetchall()
    dp.send_message(user_id, "остановить /stop")


@dp.message_handler(commands=["stop"])
def send_by(message: types.Message):
    users_list.pop(message.chat.id)
    dp.send_message(message.chat.id, "Для запуска /start")


@dp.message_handler()
def with_puree(message: types.Message):
    dp.send_message(message.chat.id, "Я тебя не понимаю. Напиши /start")


def send_messsage():
    while True:
        try:
            driver = BasketballBet()
            new_message = driver.get_live_matches()
            driver.driver_.close()
            new_message = 'None' if new_message == '' else new_message
            users = sql.execute(f"SELECT * FROM users").fetchall()
            for id in users:
                dp.send_message(id[0], new_message)
        except:
            continue

def bot_work():
    try:
        dp.polling(none_stop=True)
    except:
        pass


if __name__ == "__main__":
    threading.Thread(target=bot_work).start()
    threading.Thread(target=send_messsage).start()