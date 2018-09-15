""" Provides ease of use pickling and user registration to a db file. Mostly useful
from the command line. """
import argparse
import os

from . import Loader, DB_PATH, register_user
from .data import Database
# from .log import logger

l = Loader()


def _run():
    parser = argparse.ArgumentParser("""
This script registers new users to the database object. See
docs/developers/Database.md for object details. """)

    parser.add_argument('name', help='The name of the maker')
    parser.add_argument('ident', help='The maker\'s network identifier')

    parsed = parser.parse_args()

    if os.access(DB_PATH, os.F_OK):
        register_user(l.load(), parsed.name, parsed.ident)
    else:
        register_user(Database(), parsed.name, parsed.ident)

if __name__ == '__main__':
    _run()

    raise DeprecationWarning('Direct execution of register.py soon to be deprecated')
