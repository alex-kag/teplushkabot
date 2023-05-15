# Данный модуль читает настройки из файла конфигурации .env
import logging
# для чтения конфигурационных файлов
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)

# Нормальная работа
logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Режим отладки, пишем каждый чих
# logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)

logger.info('Начато чтение конфига')
load_dotenv()
try:
#     settings_file_lines = open(".env", mode="r").read().strip('=').split('\n')
    API_TOKEN = os.getenv('token')
    ADMIN_ID = [int(i) for i in os.getenv('adminid').replace(' ','').split(',')]
    URL_TO_GET_DATA = os.getenv('url_to_get_data')
    DB_PATH = os.getenv('db_path')

except:
    logger.critical("Не найден или некоректный файл настроек .env")
    exit(1)
