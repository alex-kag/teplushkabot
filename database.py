import sqlite3
from datetime import datetime


class DBManager:
    def __init__(self, db_path='database/teplushka.db'):
        self.db = sqlite3.connect(db_path)
        self.cur = self.db.cursor()
        self.__recreator_database()

    def __recreator_database(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        username TEXT,
        phone TEXT,
        isadmin INTEGER,
        lu TEXT)""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS reg_codes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uniq_code TEXT UNIQUE NOT NULL,
        phone TEXT,
        lu TEXT)""")

        self.db.commit()

    def new_code(self, code, phone):
        """
        вставляем в базу код для нового пользователя
        :param code:
        :param phone:
        :return:
        """
        # время запроса
        lu = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        self.cur.execute("INSERT INTO reg_codes (uniq_code, phone, lu) VALUES (?,?,?)", (code, phone, lu))
        self.db.commit()

    def find_code(self, code):
        return self.cur.execute("SELECT * FROM reg_codes WHERE uniq_code = ?", (code,)).fetchone()

    def remove_code(self, code):
        self.cur.execute("DELETE FROM reg_codes WHERE uniq_code = ?", (code,))
        self.db.commit()

    def add_user(self, user_id, username='', phone='', admin=False):
        # время запроса
        lu = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        isadmin = 0
        if admin:
            isadmin = 1

        self.cur.execute("INSERT INTO users (user_id, username, phone, isadmin, lu) VALUES (?, ?, ?, ?, ?)",
                         (user_id, username, phone, isadmin, lu))
        self.db.commit()

    def find_user_by_id(self, user_id):
        """
        Ищет id в базе
        :param user_id:
        :return:
        """
        return self.cur.execute("SELECT * FROM users WHERE user_id = ? ", (user_id,)).fetchone()

    def find_admin_by_id(self, user_id):
        """
        Ищет id в базе
        :param user_id:
        :param admin:
        :return:
        """
        isadmin = 1

        return self.cur.execute("SELECT * FROM users WHERE user_id = ? and isadmin = ? ", (user_id, isadmin)).fetchone()

    def service(self, adminid: dict):
        """
        Сервисная функция, проверяет, что бы в базе были записаны id админов, из .env

        :param adminid:
        :return:
        """
        for id in adminid:
            if self.find_admin_by_id(id) is None:
                self.add_user(id, admin=True)


#
# import asyncio
#
# import secrets
# # import random
#
# # i = random.randint(10000,999999)
# # print(i)
#
#
# # passq = secrets.token_urlsafe(10)
# # i = 0
# async def db_init():
#     """
#     Инициализация базы, при необходимости, создаем заного
#     :return:
#     """
#     global db, cur
#     db = sqlite3.connect('database/teplushka.db')
#     cur = db.cursor()
#     cur.execute("""CREATE TABLE IF NOT EXISTS users(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id INTEGER UNIQUE,
#     username TEXT,
#     phone TEXT,
#     isadmin INTEGER,
#     lu TEXT)""")
#
#     cur.execute("""CREATE TABLE IF NOT EXISTS reg_codes(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     uniq_code TEXT UNIQUE NOT NULL,
#     phone TEXT,
#     lu TEXT)""")
#
#     db.commit()
#
# async def new_code(code, phone):
#     """
#     вставляем в базу код для нового пользователя
#     :param code:
#     :param phone:
#     :return:
#     """
#     # время запроса
#     lu = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
#     cur.execute("INSERT INTO reg_codes (uniq_code, phone, lu) VALUES (?,?,?)", (code, phone, lu))
#     db.commit()
#
# async def find_code(code):
#     return cur.execute("SELECT * FROM reg_codes WHERE uniq_code = ?",(code,)).fetchone()
#
# async def remove_code(code):
#     cur.execute("DELETE FROM reg_codes WHERE uniq_code = ?",(code,))
#     db.commit()
#
# async def add_user(user_id, username='', phone='', isadmin=0):
#     # время запроса
#     lu = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
#
#     cur.execute("INSERT INTO users (user_id, username, phone, isadmin, lu) VALUES (?, ?, ?, ?, ?)",
#                 (user_id, username, phone, isadmin, lu))
#     db.commit()
#
# async def find_user_by_id(user_id):
#     return cur.execute("SELECT * FROM users WHERE user_id = ?",(user_id,)).fetchone()
#
#
# # async def get_users():
# #     return cur.execute("SELECT * FROM users").fetchall()
#
#
# asyncio.run(db_init())
#
# passq = secrets.token_urlsafe(10)
# # asyncio.run(new_code(passq,'+375297110876'))
#
# qq = asyncio.run(find_code('QNoFZnq47e-gcQ'))
#
# i=0

# db = DBManager()
# # qq = db.find_code('QNoFZnq47e-gcQ')
# rez = db.find_user_by_id(123456)
# if rez is None:
#     print(rez)
# else:
#     print("asfda")
