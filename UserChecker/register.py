""" Provides ease of use pickling and user registration to a db file. Mostly useful
from the command line. """
import argparse
import os

from . import Loader, DB_PATH, register_user
from .data import Database
# from .log import logger

l = Loader()


def _run():
    pass

if __name__ == '__main__':
    _run()

    raise DeprecationWarning('Direct execution of register.py soon to be deprecated')
