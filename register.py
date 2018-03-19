""" Provides ease of use pickling and user registration to a db file. Mostly useful
from the command line. """
import argparse
import os

try:
    from . import core
    from . import data
    from .log import logger
except SystemError:
    import core
    import data
    from log import logger

l = core.Loader()


def register_user(db, name, ident):
    """ Adds a new `data.Person` object to `db`. """
    if db is not None:
        logger.info('Registering user')
        db.add_person(data.Person(name, ident))
    else:
        logger.info('Registering user and creating db.pkl')
        db = data.Database().add_person(data.Person(name, ident))

    logger.info('Saving DB')
    l.dump(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("""
    This script registers new users to the database object. See
    docs/developers/Database.md for object details. """)

    parser.add_argument('name', help='The name of the maker')
    parser.add_argument('ident', help='The maker\'s network identifier')

    parsed = parser.parse_args()

    if os.access(core.DB_PATH, os.F_OK):
        register_user(l.load(), parsed.name, parsed.ident)
    else:
        register_user(data.Database(), parsed.name, parsed.ident)
