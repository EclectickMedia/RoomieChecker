import pickle
from os.path import expanduser, join
from os import mkdir, access, F_OK

__version__ = '0.2'

RC_PATH = expanduser('~/.UserCheckerRC')
DB_PATH = join(RC_PATH, 'db.pkl')


if not access(RC_PATH, F_OK):
    mkdir(RC_PATH)

from .data import Person, Database


class Loader:
    """ The standard interface for loading db.pkl. """
    def load(self, path=DB_PATH):
        """ Returns a data.Database object via `pickle.load(path)`. """
        with open(path, 'rb') as f:
            return pickle.load(f)

    def dump(self, db, path=DB_PATH):
        """ Dumps db to path via Pickle. """
        with open(path, 'wb+') as f:
            pickle.dump(db, f)


def __first_user():
    """ Gets basic information for first user generation. """

    return (DB_PATH, str(input('What is the name of the user? ')),
            str(input('What is the users identifier? ')))


def register_user(db_path, name, ident):
    """ Adds a new `data.Person` object to `db`. """
    db = Loader().load(DB_PATH)
    if db is not None:
        # logger.info('Registering user')
        db.add_person(Person(name, ident))
    else:
        # logger.info('Registering user and creating db.pkl')
        db = Database().add_person(Person(name, ident))

    # logger.info('Saving DB')
    Loader().dump(db, DB_PATH)


def validate_db():
    if not access(DB_PATH, F_OK):
        Loader().dump(Database())
        assert access(DB_PATH, F_OK), 'DB_FILE not made during validate'

    if type(Loader().load()) is not Database or not len(Loader().load()) >= 1:
        return False
    else:
        return True
