import time
from datetime import datetime, timedelta
import telebot
from telebot import types
import sqlite3
import db_mysql
import config

bot = telebot.TeleBot(config.api)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
gusini = db_mysql.database_initialization()
admin_list = config.admin_list
an = message.from_user.username


@bot.message_handler(commands=['start'])
def start_command(message):
    a = f'@{message.from_user.username} здравствуйте!'
    if an in admin_list:
        markup = types.ReplyKeyboardMarkup()
        btn3 = types.KeyboardButton('Массовая рассылка')
        btn4 = types.KeyboardButton('Вывести всех пользователей')
        markup.row(btn3, btn4)
        bot.send_message(message.chat.id, a)
        bot.send_message(message.chat.id, 'Вас приветствует ITeam помощник!', reply_markup=markup)
        admin_func()

    elif an not in admin_list:
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Зарегистрироваться')
        btn2 = types.KeyboardButton('Войти')
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, a)
        bot.send_message(message.chat.id, 'Вас приветствует ITeam помощник!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def admin_func(message):
    if message.text == 'Массовая рассылка':
        send_handler()
    elif message.text == 'Вывести всех пользователей':
        cursor.execute('SELECT * FROM gusini')
        users = cursor.fetchall()
        users = str(users)
        bot.send_message(message.chat.id, text=users)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == 'Зарегистрироваться':

        bot.send_message(message.chat.id, 'Сейчас тебя зарегистрируем! Введи своё имя:')
        bot.register_next_step_handler(message, user_name)
    elif message.text == 'Посмотреть своё расписание':
        cursor.execute("""
                SELECT users.user_id, users.name, courses.course_name 
                FROM user_courses
                JOIN users ON user_courses.user_id = users.user_id
                JOIN courses ON user_courses.course_id = courses.course_id
                ORDER BY users.user_id  
            """)
        current_user = None

        for (user_id, name, course_name) in cursor.fetchall():
            if current_user != user_id:
                print(f"ID пользователя: {user_id}, Имя: {name}")
                current_user = user_id
            bot.send_message(message.chat.id, text=f"  Курс: {course_name}")

    elif message.text == 'Записаться на курс':
        user_id = input("Введите идентификатор пользователя: ")
        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            print("Пользователь с таким ID не найден.")
            return

        course_id = input("Введите идентификатор курса: ")
        cursor.execute("SELECT course_id FROM courses WHERE course_id = %s", (course_id,))
        if not cursor.fetchone():
            bot.send_message(message.chat.id, text="Курс с таким ID не найден.")
            return
        cursor.execute("SELECT * FROM user_courses WHERE user_id = %s AND course_id = %s", (user_id, course_id))
        if cursor.fetchone():
            print("Пользователь уже записан на этот курс.")
            return
        cursor.execute("INSERT INTO user_courses (user_id, course_id) VALUES (%s, %s)", (user_id, course_id))
        connection.commit()
        bot.send_message(message.chat.id, text="Пользователь успешно записан на курс.")
    elif message.text == 'Информация по курсам':
        cursor.execute("SELECT * FROM courses")
        for (course_id, course_name, start_date, description_short, description_long) in cursor.fetchall():
            bot.send_message(messagw.chat.id, text=f"ID: {course_id}, Название: {course_name}, Дата начала: {start_date}\nКраткое описание: {description_short},\nПолное описание: {description_long}")

    elif message.text == 'Войти':
        bot.send_message(message.chat.id, 'Инициализация протокола входа. Введи своё имя:')
        bot.register_next_step_handler(message, user_name)
    elif message.text == 'Посмотреть своё расписание':
        cursor.execute("""
                        SELECT users.user_id, users.name, courses.course_name 
                        FROM user_courses
                        JOIN users ON user_courses.user_id = users.user_id
                        JOIN courses ON user_courses.course_id = courses.course_id
                        ORDER BY users.user_id  
                    """)
        current_user = None

        for (user_id, name, course_name) in cursor.fetchall():
            if current_user != user_id:
                print(f"ID пользователя: {user_id}, Имя: {name}")
                current_user = user_id
            bot.send_message(message.chat.id, text=f"  Курс: {course_name}")

    elif message.text == 'Записаться на курс':
        user_id = input("Введите идентификатор пользователя: ")
        cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            print("Пользователь с таким ID не найден.")
            return

        course_id = input("Введите идентификатор курса: ")
        cursor.execute("SELECT course_id FROM courses WHERE course_id = %s", (course_id,))
        if not cursor.fetchone():
            bot.send_message(message.chat.id, text="Курс с таким ID не найден.")
            return
        cursor.execute("SELECT * FROM user_courses WHERE user_id = %s AND course_id = %s", (user_id, course_id))
        if cursor.fetchone():
            print("Пользователь уже записан на этот курс.")
            return
        cursor.execute("INSERT INTO user_courses (user_id, course_id) VALUES (%s, %s)", (user_id, course_id))
        connection.commit()
        bot.send_message(message.chat.id, text="Пользователь успешно записан на курс.")

    elif message.text == 'Информация по курсам':
        cursor.execute("SELECT * FROM courses")
        for (course_id, course_name, start_date, description_short, description_long) in cursor.fetchall():
            bot.send_message(messagw.chat.id,
                text=f"ID: {course_id}, Название: {course_name}, Дата начала: {start_date}\nКраткое описание: {description_short},\nПолное описание: {description_long}")


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введи свою электронную почту:')
    bot.register_next_step_handler(message, email_number)


def email_number_tg(message):
    global email_number
    tg_id = message.from_user.username
    email_number = message.text.strip()
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован (или успешно зашёл в свой аккаунт)')
    bot.register_next_step_handler(message, answer)
    answer(message)
    db_mysql.new_user(name, email_number, tg_id)


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
    if an in admin_list:
        send_message_to_subscribers(message.text[6:])
    else:
        bot.send_message(message.chat.id, 'У вас нет прав на выполнение этой команды.')


cursor.close()
conn.close()
bot.polling(none_stop=True)
