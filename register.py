import pickle
import os
import argparse

default_db = {
    'default': {
        'is_connected': False,
        'ident': 'defalut',
    }
}


def generate_db(db):
    with open('db.pkl', 'wb') as f:
        pickle.dump(db, f)


def load_db():
    if os.access('db.pkl', os.F_OK):
        with open('db.pkl', 'rb') as f:
            return pickle.load(f)
    else:
        print('NO DATABASE AVAILABLE, GENERATING A DEFAULT DB')
        generate_db(default_db)
        return load_db()


def register_user(db, name, ident):
    print('Registering %s with identifier of \'%s\'.' % (name, ident))
    db[name] = {
        'ident': ident,
        'is_connected': False
    }

    print('Saving DB')
    generate_db(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('name', help='The name of the maker')
    parser.add_argument('ident', help='The maker\'s network identifier')

    parsed = parser.parse_args()

    register_user(load_db(), parsed.name, parsed.ident)
