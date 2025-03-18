import json
import os
from pathlib import Path

current_dir = os.getcwd()

path_file = Path("../data") / "operations.json"


def fin_transaction(json_file) -> dict:
    """
    Функция принимает json файл по относительному адресу
    предусмотрены ошибки, если файлы не найдены (сколько я времени потратил на то что не мог запустить json)
    """
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            string_json = file.read()
            data = json.loads(string_json)
            return data
    except FileNotFoundError as e:
        print(f"Файл {json_file} не найден: {e}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Ошибка при разборе JSON в файле {json_file}: {e}")
        return {}


print(fin_transaction(path_file))
