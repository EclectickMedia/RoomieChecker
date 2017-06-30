import logging
import logging.handlers as handlers

import sys  # for grabbing the program directory
import os  # for splitting sys.argv
PROGRAM_PATH = os.path.split(sys.argv[0])[0]
DEBUG_LOG_PATH = os.path.join(PROGRAM_PATH, 'logs', 'debug.log')
TESTS_LOG_PATH = os.path.join(PROGRAM_PATH, 'logs', 'tests.log')

# BEGIN Logger setup
file_formatter = logging.Formatter(
    '%(asctime)s:'
    '%(filename)-24s:'
    '%(name)-24s:'
    '%(levelname)-10s:'
    '%(funcName)-24s:'
    '%(lineno)-4d:'
    '%(message)s'
)

stream_formatter = logging.Formatter(
    '%(levelname)-10s:'
    '%(name)-20s:'
    '%(message)s'
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_formatter)
stream_handler.setLevel(logging.INFO)

tests_handler = handlers.RotatingFileHandler(TESTS_LOG_PATH,
                                             maxBytes=500000, backupCount=1)
tests_handler.setFormatter(file_formatter)
tests_handler.setLevel(logging.DEBUG)

debug_handler = handlers.RotatingFileHandler(DEBUG_LOG_PATH,
                                             maxBytes=500000, backupCount=5)
debug_handler.setFormatter(file_formatter)
debug_handler.setLevel(logging.DEBUG)

logger = logging.getLogger('base')
logger.setLevel(logging.DEBUG)
logger.addHandler(debug_handler)
logger.addHandler(stream_handler)

test_logger = logging.getLogger('base.tests')
test_logger.addHandler(tests_handler)
