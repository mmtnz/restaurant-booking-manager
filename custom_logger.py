import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler

"""
To create a custom logger
- customizable log path
- customizable log items
- customizable log level
It generates a file per day
"""

""" Logger configuration """
LOGGER_LEVEL = logging.INFO
LOG_FILES_PATH = '.'
NAME_PROGRAMME = "restaurant-booking-manager"
FOLDER_NAME = f'{NAME_PROGRAMME}-log'


logger = logging.getLogger(NAME_PROGRAMME)
logger.setLevel(LOGGER_LEVEL)
path = 'log'

if LOG_FILES_PATH != '.':
    path = os.path.join(LOG_FILES_PATH, FOLDER_NAME)

if not os.path.exists(path):
    os.makedirs(path)

file_handler = TimedRotatingFileHandler(
    os.path.join(path, '.'.join([NAME_PROGRAMME, 'log'])),
    when='midnight'
)

file_handler.namer = lambda name: name.replace(".log", "") + ".log"
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s',
                              datefmt='%d/%b/%Y %H:%M:%S')

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.info(f"[+] {NAME_PROGRAMME} logger created")
