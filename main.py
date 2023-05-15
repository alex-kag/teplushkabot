# Подключение внешних модулей
# модуль логирования
import logging

import secrets

# Импорт переменных
from aiogram import Bot, Dispatcher, executor, types

from database import DBManager

# Тут будут локальные импорты
from settings import API_TOKEN
from settings import ADMIN_ID
from settings import URL_TO_GET_DATA
from teploparser import getDataFromServer

from keyboard import button_row

# Путь к базе
from settings import DB_PATH

# Настройка лога
logger = logging.getLogger(__name__)

logger.info('Программа запущена, начинаем инициализацию')
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
db = DBManager(DB_PATH)
db.service(ADMIN_ID)

def allowed_user(userid):
    """
    Проверка разрешения для пользователя
    :param userid:
    :return:
    """
    logger.info('начата проверка на допуск пользователя')

    if db.find_user_by_id(userid) is not None:
        logger.info('доступ разрешен')
        return True
    logger.info('доступ запрещен')
    return False

def allowed_admin(userid):
    """
    Проверка разрешения для админа
    :param userid:
    :return:
    """
    logger.info('начата проверка на допуск админа')

    if db.find_admin_by_id(userid) is not None:
        logger.info('Разрешено, так как админ')
        return True
    logger.info('доступ запрещен')
    return False

def extract_unique_code(text):
    # Extracts the unique_code from the  command.
    return text.split()[1] if len(text.split()) > 1 else None

def add_userid_to_allowed(id):
    """
    Функция для добавления пользователя
    :param id:
    :return:
    """
    db.add_user(id)


@dp.message_handler(commands=['help'])
async def send_help(message :types.Message):
    """
    Вызов справки по работе с ботом
    :param message:
    :return:
    """
    logger.debug('Вызов общей справки',message.from_user.id)
    mess = ''
    if allowed_user(message.from_user.id) is None:
        logger.info('доступ запрещен')
        return
    elif allowed_admin(message.from_user.id):
        mess += 'админу доступна справка по работе с пользователями:\n'
        mess += '/help_admin:\n'

    mess += "Справка по работе с ботом Теплушка\n"
    mess += "/help эта справка\n"
    mess += "/voda параметры расхода воды\n"
    await message.answer(mess, reply_markup=button_row)

@dp.message_handler(commands=['help_admin'])
async def send_help(message :types.Message):
    """
    Вызов справки админа по работе с ботом
    :param message:
    :return:
    """
    logger.debug('Вызов админской справки',message.from_user.id)
    mess = ''
    if allowed_admin(message.from_user.id) is None:
        logger.info('доступ запрещен')
        return

    mess += '/add_new_user  номер_телефона   создать нового пользователя \n'
    mess += '/delete  telegram_id   удалить пользователя \n'

    mess += "Справка по работе с ботом Теплушка\n"
    mess += "/help эта справка\n"
    mess += "/voda параметры расхода воды\n"
    await message.answer(mess, reply_markup=button_row)

@dp.message_handler(commands=['add_new_user'])
async def add_new_user(message :types.Message):
    """
    создание кода для нового пользователя
    :param message:
    :return:
    """
    logger.info('создание нового пользователя вызвано',message.from_user.id)
    if allowed_admin(message.from_user.id) is None:
        logger.info('доступ запрещен')
        return
    phone_number = extract_unique_code(message.text)
    if phone_number is None:
        await message.answer('Команда имеет вид: /add_new_user  номер_телефона')
        return
    uniq_code = secrets.token_urlsafe(10)
    db.new_code(uniq_code,phone_number)
    mess = 'Для получения параметров теплосети, пройдите по ссылке и зарегистрируйтесь у бота\n'
    mess += f'https://t.me/teplushka_bot?start={uniq_code}'
    await message.answer(mess)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    Стартовая команда бота, должна проходить только по специально сгенерированной ссылке, с кодом, в противном случае
    пользователь не сможет зарегистрироваться у бота
    :param message:
    :return:
    """
    if allowed_user(message.from_user.id):
        await message.answer('Добро пожаловать. Я бот для выдачи параметров работы теплосети')
    else:
        uniq_code = extract_unique_code(message.text)
        if db.find_code(uniq_code) is not None:
            add_userid_to_allowed(message.from_user.id)
            db.remove_code(uniq_code)
            await message.answer('Добро пожаловать. Я бот для выдачи параметров работы теплосети',reply_markup=button_row)
        else:
            await message.answer('Извините, но вам запрещен доступ. Обратитесь к системному администратору')
    if allowed_admin(message.from_user.id):
        logger.info('У нас админ, отсылаем ему админскую клаву')
        await message.answer('sfsd',reply_markup=button_row)

@dp.message_handler(commands=['voda'])
async def send_welcome(message: types.Message):
    """
    Основная работа бота - выдает текущие параметры работы теплосети
    :param message:
    :return:
    """
    if allowed_user(message.from_user.id):
        # Формируем запрос и ответ от базы
        logger.info('Запрос на получение параметров от', message.from_user.id)
        await message.answer(getDataFromServer(URL_TO_GET_DATA),parse_mode='HTML')
    else:
        logger.info('Какой-то левый запрос')


logger.info('Запущен главный цикл')
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)




