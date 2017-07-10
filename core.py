#! /Library/Frameworks/Python.framework/Versions/3.5/bin/python3
import pickle
import subprocess
import time
from tempfile import NamedTemporaryFile

try:
    from .log import logger
except SystemError:
    from log import logger

# CONSTANTS
CONNECTION_CONFIRM = 1200  # 20 minutes in seconds
DISCONNECTION_CONFIRM = 3600  # 1 hour in seconds
ERR_FILE = NamedTemporaryFile('a+')
OUT_FILE = NamedTemporaryFile('a+')
DB_PATH = 'db.pkl'


class Loader:
    """ The standard interface for loading db.pkl. """
    def load(self, path='db.pkl'):
        """ Loads a dict object containing the following fields:

            name - The name of the maker
            ident - The unique network identifier.
            is_connected - True if user is on the wifi, false otherwise.
        """
        with open(path, 'rb') as f:
            return pickle.load(f)

    def dump(self, db, path='db.pkl'):
        """ Dumps db to path via Pickle. """
        with open(path, 'wb+') as f:
            pickle.dump(db, f)


class UserChecker:
    """ Handles user connectivity searching.

    Checks output_file for person.iter occurances from people that have been
    loaded from the database.

    Presents an iter interface to allow for easily running the for loop. Each
    iteration of __iter__ yields the person object that was used.

    Also presents a callback feature to allow for easy data collection, without
    requiring the calling method to track connection policies themselves. """

    def __init__(self, db, func, quiet=False, output_file=OUT_FILE):
        """ Stores data that must be persistent.

        db = A database object loaded by Loader.load.
        func = The callback function.
        quiet = Verbosity flag.
        output_file = The file to check for user connectivity.
        """

        self.func = func
        self.db = db
        self.quiet = quiet
        self.output_file = OUT_FILE

    def grep_output(self, term, output_file=OUT_FILE, quiet=False):
        """ Parses a file for the appearance of term. This signifies that NMAP
        found the user in its scan, and we can infer they have connected to the
        network. """

        for line in output_file:
            logger.debug(str(line).strip('\n'))
            if line.count(term):
                logger.debug('%s present' % term)
                return True

        else:
            logger.debug('%s not present' % term)
            return False

    def announce(self, person):
        """ Calls self.func (the callback function), passing it a data.Person
        object. """

        self.func(person)

    def check_for_people(self, db, quiet):
        """ Checks OUT_FILE for the presence of each data.Person object's
        identifier field to identify if they are connected to the network, then
        yields each person.

        It requires a database object provided by Loader.load, and a quiet flag
        (for signalling verbosity).
        """

        for person in db.yield_people():
            logger.debug('check %s' % person.name)
            logger.debug(str(list(person)))

            if not quiet:
                logger.info('Grepping output for %s using the search term %s.'
                            % (person.name, person.ident))

            with open(OUT_FILE.name) as f:
                logger.debug('got OUT_FILE')

                if self.grep_output(person.ident, f, quiet):

                    if not person.is_connected:

                        if not quiet and person.connection_started == 0.0:
                            logger.info('%s connected to the WiFi!'
                                        % person.name)

                        person.is_connected = True  # sets connection_started
                        person.last_connected = time.time()

                        logger.debug('%s: %s %s %s'
                                     % (person.name, str(person.is_connected),
                                        str(person.last_connected),
                                        str(person.connection_started)))
                        yield person
                    else:
                        # We disregard their appearance if they are already
                        # connected, unless they have been connected long enough
                        logger.debug('%s present, already connected: %s'
                                     % (person.name, person.is_connected))

                        person.last_connected = time.time()
                        if person.connection_started != 0.0:
                            logger.debug("connection confirmation: %s %s",
                                         time.time() -
                                         person.connection_started,
                                         CONNECTION_CONFIRM)
                            if time.time() - person.connection_started > \
                                    CONNECTION_CONFIRM and not person.announced:
                                self.announce(person)  # TODO needs to track
                                person.announced = True

                        logger.debug('%s: %s %s %s'
                                     % (person.name, str(person.is_connected),
                                        str(person.last_connected),
                                        str(person.connection_started)))

                        yield person

                else:  # If they are not present

                    # If person was previously connected, we can assume they
                    # have disconnected form the network
                    logger.debug('%s previously connected: %s'
                                 % (person.name, person.is_connected))

                    if not quiet:
                        logger.info('%s disconnected from the WiFi!'
                                    % person.name)

                    logger.debug('%s not present, ensure data' % person.name)
                    person.is_connected = False
                    # is up to date. This is to ensure a clean runtime.

                    # How long ago were they connected?
                    if person.connection_started != 0.0:  # connection active
                        logger.debug('disconnection confirmation: %s %s',
                                     time.time() - person.last_connected,
                                     DISCONNECTION_CONFIRM)
                        if time.time() - person.last_connected > \
                                DISCONNECTION_CONFIRM and not person.announced:
                            self.announce(person)  # TODO needs track announced
                            person.announced = True
                            person.connection_started = 0.0

                    yield person

    def __iter__(self):
        for person in self.check_for_people(self.db, self.quiet):
            yield person


def reset(db):
    """ Resets data fields all users in the database. """
    db = Loader().load()
    for person in db.yield_people():
        person.is_connected = False
        person.last_connected = 0.0
        person.connection_started = 0.0
        person.announced = False
    Loader().dump(db)

    ERR_FILE.truncate(0)
    OUT_FILE.truncate(0)


def generate_nmap(output_file=OUT_FILE, ip_range='192.168.1.0/24'):
    """ Returns a subprocess.Popen object running an NMAP request.

    Outputs all results to output_file. """

    return subprocess.Popen(['nmap', '-sP', ip_range], stdout=output_file,
                            stderr=ERR_FILE)


if __name__ == '__main__':
    DeprecationWarning('Direct execution of core has been deprecated! Use '
                       'main.py')
