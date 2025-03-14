import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='sasyn2008')

cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS education")
cursor.execute("USE education")

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email_number VARCHAR(100) NOT NULL,
    tg_id INT(100) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    description_short VARCHAR(100) NOT NULL,
    description_long VARCHAR(100) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_courses (
    user_id INT,
    course_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id),
    PRIMARY KEY (user_id, course_id)
)
""")

def new_user():
    name = input("Введите имя пользователя: ")
    email_number = input("Введите email или телефон: ")
    tg_id = input("Введите Telegramm_id: ")
    cursor.execute("INSERT INTO users (name, email_number, tg_id) VALUES (%s, %s, %s)", (name, email_number, tg_id))
    connection.commit()

def new_curs():
    course_name = input("Введите название курса: ")
    start_date = input("Введите дату начала курса (YYYY-MM-DD): ")
    description_short = input("Введите краткое описание курса: ")
    description_long = input("Введите полное описание курса: ")
    cursor.execute("INSERT INTO courses (course_name, start_date,description_short,description_long) VALUES (%s, %s, %s, %s)", (course_name, start_date,description_short,description_long))
    connection.commit()

def user_plus_curs():
    print_user()
    user_id = input("Введите идентификатор пользователя: ")
    cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
    if not cursor.fetchone():
        print("Пользователь с таким ID не найден.")
        return
    print_curs()
    course_id = input("Введите идентификатор курса: ")
    cursor.execute("SELECT course_id FROM courses WHERE course_id = %s", (course_id,))
    if not cursor.fetchone():
        print("Курс с таким ID не найден.")
        return
    cursor.execute("SELECT * FROM user_courses WHERE user_id = %s AND course_id = %s", (user_id, course_id))
    if cursor.fetchone():
        print("Пользователь уже записан на этот курс.")
        return
    cursor.execute("INSERT INTO user_courses (user_id, course_id) VALUES (%s, %s)", (user_id, course_id))
    connection.commit()
    print("Пользователь успешно записан на курс.")

def print_user():
    cursor.execute("SELECT * FROM users")
    for (user_id, name, email_number,tg_id) in cursor.fetchall():
        print(f"ID: {user_id}, Имя: {name}, Email/Телефон: {email_number},Telegramm_id: {tg_id}")

def print_curs():
    cursor.execute("SELECT * FROM courses")
    for (course_id, course_name, start_date, description_short, description_long) in cursor.fetchall():
        print(f"ID: {course_id}, Название: {course_name}, Дата начала: {start_date}\nКраткое описание: {description_short},\nПолное описание: {description_long}")


def print_user_plus_curs():
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
        print(f"  Курс: {course_name}")

while True:
    print("1) Добавить пользователя")
    print("2) Добавить курс")
    print("3) Записать пользователя на курс")
    print("4) Вывести всех пользователей")
    print("5) Вывести все курсы")
    print("6) Вывести пользователей + курсы")
    choice = input("Введите номер действия: ")
    if choice == '1':
        new_user()
    elif choice == '2':
        new_curs()
    elif choice == '3':
        user_plus_curs()
    elif choice == '4':
         print_user()
    elif choice == '5':
        print_curs()
    elif choice == '6':
        print_user_plus_curs()
    else:
        print("Неверный ввод, попробуйте снова.")

cursor.close()
connection.close()
