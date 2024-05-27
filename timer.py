import telebot
import schedule
import time
import datetime as dt
import sqlite3
from database import big_data
from week import switch_variable_weekly

current_value = 0
bot = telebot.TeleBot('6490583743:AAH5UR-Sw9QgL_bi2hzfVBzTdKgdcP-_h7Q')
qw = switch_variable_weekly(current_value)
def send_message():
    conn = sqlite3.connect('user_id.db')
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, * FROM id")
    iteams = cursor.fetchall()
    conn.commit()
    conn.close()
    utc_time = dt.datetime.utcnow()
    period = dt.timedelta(hours=5)
    astana_time = utc_time + period
    data = dt.date.today()
    week = data.weekday()
    time = astana_time.strftime('%H:%M')
    for id in iteams:
        chat_id = id[1]
        if time == '08:55':
            bot.send_message(chat_id, f'следущая пара {big_data[qw][week][0]["name"]} {big_data[qw][week][0]["description"]}')
        elif time == '10:25':
            bot.send_message(chat_id, f'следущая пара {big_data[qw][week][1]["name"]} {big_data[qw][week][1]["description"]}')
        elif time == '12:05':
           bot.send_message(chat_id, f'следущая пара {big_data[qw][week][2]["name"]} {big_data[qw][week][2]["description"]}')
        elif time == '14:05':
           bot.send_message(chat_id, f'следущая пара {big_data[qw][week][3]["name"]} {big_data[qw][week][3]["description"]}')
        else:
            bot.send_message(chat_id,'Ошибка')


# Задаем время отправки сообщения
schedule.every().day.at("08:55").do(send_message)
schedule.every().day.at("10:25").do(send_message)
schedule.every().day.at("12:05").do(send_message)
schedule.every().day.at("14:05").do(send_message)


# Бесконечный цикл для проверки расписания
while True:
    schedule.run_pending()
    time.sleep(1)
