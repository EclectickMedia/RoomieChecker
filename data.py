class Database:
    def add_person(self, person):
        self.people.append(person)
        self.names.append(person.name)

    def yield_people(self):
        for person in self.people:
            yield person

    def remove_person(self, name):
        to_remove = []

        try:
            for person in self.yield_people():
                if person.name.count(name):
                    to_remove.append(person)

            for person in to_remove:
                self.people.remove(person)

            return True
        except:
            return False

    def version(self):
        return 1

    def __init__(self):
        self.people = []
        self.names = []


class Person:
    is_connected = False
    connection_started = 0.0
    last_connected = 0.0
    announced = False

    def __init__(self, name, ident):
        if type(name) is not str:
            raise TypeError('name must be str')

        if type(ident) is not str:
            raise TypeError('ident must be string')

        self.name = name

        self.ident = ident