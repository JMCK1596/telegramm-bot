import telebot
from telebot import types
import sqlite3
import datetime as dt
from database import big_data
from week import switch_variable_weekly

bot = telebot.TeleBot('6490583743:AAH5UR-Sw9QgL_bi2hzfVBzTdKgdcP-_h7Q')
current_value = 0
qw = switch_variable_weekly(current_value)
@bot.message_handler(commands=['register'])
def register(message):
     conn = sqlite3.connect('user_id.db')
     cursor = conn.cursor()
     cursor.execute("""
     CREATE TABLE IF NOT EXISTS id(
     chat_id INTEGER UNIQUE
     )""")

     chat_id = message.chat.id
     try:
        cursor.execute("INSERT INTO id (chat_id) VALUES (?)", (chat_id,))
        conn.commit()
        bot.send_message(chat_id, 'ваш chat id теперь в базе данных')
     except sqlite3.IntegrityError:
         bot.send_message(chat_id,'Защита от идиотов активирована')
     conn.commit()
     conn.close()

@bot.message_handler(commands=['start'])

def start(message):
     markup = types.ReplyKeyboardMarkup()
     but1 = types.KeyboardButton('Первая пара')
     but2 = types.KeyboardButton('Вторая пара')
     markup.row(but1,but2)
     but3 = types.KeyboardButton('Третья пара')
     but4 = types.KeyboardButton('Четвертая пара')
     markup.row(but3,but4)
     but5 = types.KeyboardButton('Сегоднишние пары')
     but6 = types.KeyboardButton('Завтрашние пары')
     markup.row(but5,but6)
     but7 = types.KeyboardButton('Какая неделя')
     markup.row(but7)
     first_name = message.from_user.first_name
     chat_id = message.chat.id
     bd = sqlite3.connect('user_id.db')
     cursor = bd.cursor()
     cursor.execute("SELECT * FROM id")
     id = cursor.fetchall()


     if chat_id == 1627036830:
          bot.send_message(message.chat.id,f'id всех кто зарегалься  {id}',reply_markup=markup)
     else:
         bot.send_message(message.chat.id, f'Привет {first_name} ',reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def photo(message):
     photo = open('./mem.jpg','rb')
     bot.send_message(message.chat.id,'я тоже могу фотки кидать')
     bot.send_photo(message.chat.id,photo)


@bot.message_handler(content_types=['audio'])
def audio(message):
     audio = open(r'./egor.mp3', 'rb')
     bot.send_message(message.chat.id, 'лучше это послушай')
     bot.send_audio(message.chat.id, audio)

@bot.message_handler()
def on_click(message):
     text = message.text
     data = dt.date.today()
     week = data.weekday()
     if text == 'Первая пара':
         bot.send_message(message.chat.id,
                          f'Первая пара {big_data[qw][week][0]["name"]} {big_data[qw][week][0]["description"]} ')
     elif text == 'Вторая пара':
         bot.send_message(message.chat.id,
                          f'Вторая пара {big_data[qw][week][1]["name"]} {big_data[qw][week][1]["description"]}')
     elif text == 'Третья пара':
         bot.send_message(message.chat.id,
                          f'Третья пара {big_data[qw][week][2]["name"]} {big_data[qw][week][2]["description"]}')
     elif text == 'Четвертая пара':
         bot.send_message(message.chat.id,
                          f'Четвертая пара {big_data[qw][week][3]["name"]} {big_data[qw][week][3]["description"]} ')
     elif text == 'Какая неделя':
         if qw == 1:
            bot.send_message(message.chat.id,
                          f'Это неделя числитель')
         elif qw == 0:
             bot.send_message(message.chat.id,'это неделя знаменатель')

     try:
         if text == 'Сегоднишние пары':
            for i in big_data[qw][week]:
               bot.send_message(message.chat.id, f'{i["name"]}')
         elif text == 'Завтрашние пары':
            for para in big_data[qw][week + 1]:
               bot.send_message(message.chat.id, f'{para["name"]}')
     except:
         for mon in big_data[qw][0]:
             bot.send_message(message.chat.id,f'{mon["name"]}')


bot.polling(none_stop=True)





