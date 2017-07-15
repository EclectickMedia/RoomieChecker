import time
try:
    from .log import logger
except SystemError:
    from log import logger


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
    """ Handles all data for each Person in the database. Provides an easy
    iterable interface to retrieve all data fields.

    For example:
        >>> from data import Person
        >>> p = Person('Ariana', 'Arianas-Device')
        >>> for field in p:
        ...     print(field)
        ('connection_announced', False)
        ('connection_started', 0.0)
        ('disconnection_announced', False)
        ('ident', 'Arianas-Device')
        ('is_connected', False)
        ('last_connected', 0.0)
        ('name', 'Ariana')
    """
    last_connected = 0.0  # TODO Do we need a null interface for this?

    @property
    def is_connected(self):
        """ True if the user is currently connected.

        If set to false, and self.connection_started is equal to 0.0, sets
        self.connection_stated to time.time(). """

        return self._is_connected

    @is_connected.setter
    def is_connected(self, boolean):
        logger.debug(boolean)
        if boolean:
            if self.connection_started == 0.0:
                logger.debug('set self.connection_started = %s'
                             % self.connection_started)
                self.connection_started = time.time()

        self._is_connected = boolean

    @property
    def connection_started(self):
        """ The time at which the user connected. A value of 0.0 can be
        considered "never".

        Can be set to 0.0 when the user has been confirmed to have disconnected.
        """

        return self._connection_started

    @connection_started.setter
    def connection_started(self, time):
        logger.debug(time)
        if type(time) is not float:
            raise TypeError('time must be float')

        self._connection_started = time

    @property
    def connection_announced(self):
        """ True if the connection has been confirmed, and the status has been
        announced.

        Also resets self.disconnection_confirmation when True. """

        return self._connection_announced

    @connection_announced.setter
    def connection_announced(self, boolean):
        if boolean:
            self.disconnection_announced = False

        self._connection_announced = boolean

    @property
    def disconnection_announced(self):
        """ True if the disconnection has been confirmed, and the status has
        been announced.

        Also resets self.connection_announced when True. """

        return self._disconnection_announced

    @disconnection_announced.setter
    def disconnection_announced(self, boolean):
        if self.connection_announced:
            self.connection_announced = False

        self._disconnection_announced = boolean

    def __init__(self, name, ident):
        if type(name) is not str:
            raise TypeError('name must be str')

        if type(ident) is not str:
            raise TypeError('ident must be string')

        self.name = name

        self.ident = ident

        self._connection_started = 0.0

        self._is_connected = False

        self._connection_announced = False

        self._disconnection_announced = False

    def __iter__(self):
        for attr in dir(self):
            if not attr[0:1].count('_'):
                yield (attr, getattr(self, attr))
