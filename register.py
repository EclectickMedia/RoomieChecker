import argparse

import core
import data

l = core.Loader()

def register_user(db, name, ident):
    if db is not None:
        print('Registering user')
        db.add_person(data.Person(name, ident))
    else:
        print('Registering user and creating db.pkl')
        db = data.Database().add_person(data.Person(name, ident))
    print('Saving DB')
    l.dump(db)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("""
    This script registers new users to the database object. See
    docs/developers/Database.md for object details. """)

    parser.add_argument('name', help='The name of the maker')
    parser.add_argument('ident', help='The maker\'s network identifier')

    parsed = parser.parse_args()

    register_user(l.load(), parsed.name, parsed.ident)
