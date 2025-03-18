import time
from datetime import datetime, timedelta
import telebot
from telebot import types
import sqlite3
bot = telebot.TeleBot('7959873800:AAH2pgOXXef0g6cm2fXLz54c38KZ-3TXb7E')
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

@bot.message_handler(commands=['start'])
def start_command(message):
    a = f'@{message.from_user.username} здравствуйте!'
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Зарегистрироваться', )
    btn2 = types.KeyboardButton('Войти')
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, a)
    bot.send_message(message.chat.id, 'Вас приветствует ITeam помощник!', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):

    if (message.text == 'Зарегистрироваться'):

        bot.send_message(message.chat.id, 'Сейчас тебя зарегистрируем! Введи своё имя:')
        bot.register_next_step_handler(message, user_name)
    elif message.text == 'Посмотреть своё расписание':
        bot.send_message(message.chat.id, text="Всё ок")
    elif (message.text == 'Записаться на курс'):
        bot.send_message(message.chat.id, text="Всё ок")
    elif (message.text == 'Информация по курсам'):
        bot.send_message(message.chat.id, text="Всё ок")

    elif (message.text == 'Войти'):
        bot.send_message(message.chat.id, 'Сейчас тебя 100100100111001 в нашу программу! Введи своё имя:')
        bot.register_next_step_handler(message, user_name)
    elif message.text == 'Посмотреть своё расписание':
        bot.send_message(message.chat.id, text="Всё ок")
    elif (message.text == 'Записаться на курс'):
        bot.send_message(message.chat.id, text="Всё ок")
    elif (message.text == 'Информация по курсам'):
        bot.send_message(message.chat.id, text="Всё ок")
    elif (message.text == 'Посмотреть своё расписание'):
        bot.send_message(message.chat.id, text="Всё ок")

    elif (message.text == 'Записаться на курс'):
        bot.send_message(message.chat.id, text="Всё ок")

    elif message.text == 'Информация по курсам':
        bot.send_message(message.chat.id, text="Всё ок")
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введи свой пароль:')
    bot.register_next_step_handler(message, user_pass)
def user_pass(message):
    password = message.text.strip()
    bot.send_message(message.chat.id, 'Введи свой номер телефона:')
    bot.register_next_step_handler(message, user_p_n)
def user_p_n(message):
    p_n = message.text.strip()
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован (или успешно зашёл в свой аккаунт)')
    bot.register_next_step_handler(message, answer)
    answer(message)
def answer(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Посмотреть своё расписание")
    btn2 = types.KeyboardButton("Записаться на курс")
    btn3 = types.KeyboardButton("Информация по курсам")
    markup.row(btn1)
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, text="Что хочешь сделать?", reply_markup=markup)
def send_message_to_subscribers(message):
    cursor.execute('SELECT chat_id FROM users WHERE subscribed = 1')
    rows = cursor.fetchall()
    for row in rows:
        chat_id = row
        try:
            bot.send_photo(message.chat.id, photo, caption='Ваш текст')
        except Exception as e:
            print(f'Ошибка в отправке сообщения {chat_id}: {e}')
def send_notification(student_name, days_until_lesson):
    print(f"Напоминание для {student_name}: до начала урока осталось {days_until_lesson} дней.")


def notification_func(students_list: list):
    today = datetime.today().date()
    for student in students_list:
        start_date = datetime.strptime(student["start_date"], "%Y-%m-%d").date()

        weeks_passed = (today - start_date).days // 7
        next_lesson_date = start_date + timedelta(weeks=weeks_passed + 1)
        delta = (next_lesson_date - today).days

        if delta == 3:
            send_notification(student["name"], delta)


    while True:
        notification_func(students)
        time.sleep(86400)

@bot.message_handler(commands=['send'])
def send_handler(message):
    if message.chat.id == 'hylo_x2':
        send_message_to_subscribers(message.text[6:])
    else:
        bot.send_message(message.chat.id, 'У вас нет прав на выполнение этой команды.')
bot.polling(none_stop=True)