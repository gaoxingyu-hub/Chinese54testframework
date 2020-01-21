import logging.config
from logging.handlers import TimedRotatingFileHandler
from os import path
import frozen_dir
import re

SETUP_DIR = frozen_dir.app_path()
class Logger:

    """
    python log module
    methods:
    add this import information:
    from common.logConfig import Logger
    logger = Logger.module_logger("com_control_device")
    """
    def __init__(self):
        return

    @classmethod
    def module_logger(self,module_name):
        """
        output log to files
        :param module_name: log file module,you can define
        different file for different modules
        :return: logger object
        """

        log_file_directory = path.join(SETUP_DIR, "logs", module_name + ".log")
        logger = logging.getLogger("logger")
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        log_file_handler = TimedRotatingFileHandler(filename=log_file_directory, when="D", interval=1, backupCount=7)
        log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
        log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
        log_file_handler.setFormatter(formatter)
        log_file_handler.setLevel(logging.DEBUG)

        logger.addHandler(log_file_handler)
        return logger

    @classmethod
    def debug_logger(self):
        """
        output console log
        :return:
        """


        logger = logging.getLogger("logger")
        handler = logging.StreamHandler()
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger

