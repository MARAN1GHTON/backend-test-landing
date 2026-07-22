import logging
import sys
import os

# Создаем директорию для логов, если ее нет
os.makedirs("data", exist_ok=True)

logger = logging.getLogger("backend_test")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Обработчик для вывода в консоль
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# Обработчик для записи в файл
file_handler = logging.FileHandler("data/app.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
