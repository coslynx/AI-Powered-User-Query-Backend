import logging
import sys
from logging.handlers import RotatingFileHandler
from config.settings import settings

class Logger:
    """
    Singleton class for managing the application's logging system.
    """

    __instance = None

    def __init__(self):
        if Logger.__instance is not None:
            raise Exception("Logger class is a singleton!")
        else:
            Logger.__instance = self
            self._init_logger()

    @staticmethod
    def get_logger():
        """
        Static method to retrieve the singleton logger instance.
        """
        if Logger.__instance is None:
            Logger()
        return Logger.__instance

    def _init_logger(self):
        """
        Private method to configure the logger and handlers.
        """
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO if settings.DEBUG else logging.INFO)

        file_handler = RotatingFileHandler(
            settings.LOG_FILE_PATH,
            maxBytes=settings.LOG_FILE_MAX_SIZE,
            backupCount=settings.LOG_FILE_BACKUP_COUNT,
        )
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

logger = Logger.get_logger()