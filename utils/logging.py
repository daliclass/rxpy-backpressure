from logging import getLogger
from os import getenv


class Logger:
    def __init__(self):
        logger_name = getenv("BP_LOGGING")
        self.__logger = getLogger(logger_name) if getenv("BP_LOGGING") else None

    def warning(self, message: str = ""):
        if self.__logger:
            self.__logger.warning(message)
