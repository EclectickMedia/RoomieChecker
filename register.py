import argparse
import os
import pickle

import data


def save_db(db):
    with open('db.pkl', 'wb') as f:
        pickle.dump(db, f)


def load_db():
    if os.access('db.pkl', os.F_OK):
        with open('db.pkl', 'rb') as f:
            return pickle.load(f)
    else:
        return None


def register_user(db, name, ident):
    if db is not None:
        print('Registering user')
        db.add_person(data.Person(name, ident))
    else:
        print('Registering user and creating db.pkl')
        db = data.Database().add_person(data.Person(name, ident))
    print('Saving DB')
    save_db(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("""
    This script registers new users to the database object. See
    docs/developers/Database.md for object details. """)

    parser.add_argument('name', help='The name of the maker')
    parser.add_argument('ident', help='The maker\'s network identifier')

    parsed = parser.parse_args()

    register_user(load_db(), parsed.name, parsed.ident)
