import logging
import os
from pathlib import Path

from src.decorators import log

# Определяем путь к корню проекта
project_root = Path(__file__).resolve().parent.parent

# Определяем путь к папке logs в корне проекта
log_directory = project_root / "logs"

# Проверяем наличие папки logs и создаем ее, если она отсутствует
if not log_directory.is_dir():
    log_directory.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=os.path.join(log_directory, "application.log"),  # Указываем путь к файлу в папке logs
    filemode="w",  # Перезапись файла при каждом запуске
    encoding="utf-8",
)
auth_logger = logging.getLogger(__name__)


@log("log_test_file")
def get_mask_card_number(num_card: str) -> str:
    if len(num_card) != 16:
        auth_logger.info("Ошибка некорректной длинны номера")
        raise ValueError("Некорректная длинна номера")
    """Принимает на вход номер карты и возвращает ее маску  XXXX XX** **** XXXX"""
    return num_card[0:4] + " " + num_card[4:6] + "**" + " **** " + num_card[-4:]


def get_mask_account(small_num_card: str) -> str:
    auth_logger.info("Логирование начато.")
    if len(small_num_card) != 20:
        auth_logger.info("Ошибка некорректной длинны номера")
        raise ValueError("Некорректная длинна номера счета")
    """Принимает на вход номер карты и возвращает ее маску **XXXX"""
    return "**" + small_num_card[-4:]
