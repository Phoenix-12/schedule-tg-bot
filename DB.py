class DB:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='your_user',
            password='your_password',
            database='your_database'
        )
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def get_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return self.cursor.fetchone()

    def get_course(self, course_id):
        self.cursor.execute("SELECT * FROM courses WHERE id = %s", (course_id,))
        return self.cursor.fetchone()

    def add_on_course(self, user_id, course_id):
        self.cursor.execute("INSERT INTO user_courses (user_id, course_id) VALUES (%s, %s)", (user_id, course_id))
        self.conn.commit()
        return f"Пользователь {user_id} добавлен на курс {course_id}"

    def add_course(self, course_name):
        self.cursor.execute("INSERT INTO courses (name) VALUES (%s)", (course_name,))
        self.conn.commit()
        print(f"Курс {course_name} добавлен")

    def edit_course(self, course_name, class_date):
        self.cursor.execute("UPDATE courses SET class_date = %s WHERE name = %s", (class_date, course_name))
        self.conn.commit()
        print(f"Курс {course_name} обновлен с датой {class_date}")

    def delete_course(self, course_name):
        self.cursor.execute("DELETE FROM courses WHERE name = %s", (course_name,))
        self.conn.commit()
        print(f"Курс {course_name} удален")

    def get_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        for user in users:
            print(user)
        return users