import json
import logging
import os
from pathlib import Path

# Определяем путь к корню проекта
project_root = Path(__file__).resolve().parent.parent

# Определяем путь к папке logs в корне проекта
log_directory = project_root / "logs"

# Проверяем наличие папки logs и создаем ее, если она отсутствует
if not log_directory.is_dir():
    log_directory.mkdir(parents=True, exist_ok=True)

# Основная конфигурация logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=os.path.join(log_directory, "application.log"),  # Указываем путь к файлу в папке logs
    filemode="w",  # Перезапись файла при каждом запуске
    encoding="utf-8",
)
utils_logger = logging.getLogger(__name__)

current_dir = os.getcwd()
path_file = Path("../data") / "operations.json"


def fin_transaction(json_file) -> list:
    """
    Функция принимает json файл по относительному адресу
    предусмотрены ошибки, если файлы не найдены (сколько я времени потратил на то что не мог запустить json)
    """
    try:
        utils_logger.info("Начало функции")
        with open(json_file, "r", encoding="utf-8") as file:
            string_json = file.read()
            data = json.loads(string_json)
            return data
    except FileNotFoundError as e:
        print(f"Файл {json_file} не найден: {e}")
        utils_logger.exception(e)
        return []
    except json.JSONDecodeError as e:
        utils_logger.exception(e)
        print(f"Ошибка при разборе JSON в файле {json_file}: {e}")
        return []


print(fin_transaction(path_file))
