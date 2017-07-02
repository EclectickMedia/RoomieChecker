class Database:
    """ Defines the behaviour of the database. """
    def add_person(self, person):
        """ Adds a Person object to the internal people list. """
        self.people.append(person)

    def yield_people(self):
        """ Yields each Person object in the internal people list one at a
        time. """
        for person in self.people:
            yield person

    def remove_person(self, name):
        """ Checks each person in the internal people list for name and if
        that person's name matches the name argument, remove it from the
        internal people list. """
        try:
            for person in self.yield_people():
                if person.name.count(name):
                    self.people.remove(person)
            return True
        except:
            return False

    def version(self):
        return 1

    def __init__(self):
        self.people = []  # the internal people list


class Person:
    is_connected = False

    @property
    def connection_started(self):
        return self._connection_started

    @connection_started.setter
    def connection_started(self, time):
        if time is None:
            self._connection_started = None  # Null? SHould this be 0?

        elif type(time) is not int:
            raise TypeError('time must be int')

    last_connected = 0.0  # TODO Do we need a null interface for this?
    announced = False

    def __init__(self, name, ident):
        if type(name) is not str:
            raise TypeError('name must be str')

        if type(ident) is not str:
            raise TypeError('ident must be string')

        self.name = name

        self.ident = ident

        self._connection_started = 0.0
