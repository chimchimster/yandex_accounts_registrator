import os
import logging

from datetime import date


class Logger:
    """ Class responsible for logging exceptions """

    # Setting up logger
    yandex_registrator = logging.getLogger('YANDEX_REGISTRATOR')

    @classmethod
    def configurate(cls):
        # Set logger level
        cls.yandex_registrator.setLevel(logging.WARNING)

        # Changing directory to /logs
        os.chdir('./logs')

        # Set saving directory
        file_handler = logging.FileHandler(os.getcwd() + f'/history/yandex_logger_{date.today()}.log', mode='a')

        # Set formater
        formater = logging.Formatter('%(name)s - %(asctime)s - %(message)s')

        # Adding formater to handler
        file_handler.setFormatter(formater)

        # Adding handler to logger
        cls.yandex_registrator.addHandler(file_handler)

    @property
    def logger(self):
        return self.yandex_registrator


