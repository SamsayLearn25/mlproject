import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log"
log_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(log_path, exist_ok=True)

log_file_path = os.path.join(log_path, LOG_FILE)

log_format = "[ %(asctime)s %(lineno)s - %(levelname)s - %(message)s]"

logging.basicConfig(
    level=logging.INFO,
    filename=log_file_path,
    format=log_format,
    
)

from src.exception import CustomException
import sys
if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        logging.info("Divide by zero")
        raise CustomException(e, sys)
    