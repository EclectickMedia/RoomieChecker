#! /Library/Frameworks/Python.framework/Versions/3.5/bin/python3
""" Provides a method to check if a user is for sure connected (and using) a network.

Copyright Ariana Giroux, 2018 under the MIT license.

Uses NMAP to check the network for specified identifiers. Implements a callback
interface to notify user when the connection can be considered "confirmed."

*NOTE* Due to the how mobile devices use wireless networks, we must ensure that
we "confirm" that an identifier has an active session on the network. This is
handled by ensuring that a user has been on the network for a particular amount
of time (20 minutes by default).

*NOTE* To look at the logic behind the "confirmation" policies, check
`./UserChecker - Confirmation Policies.pdf`.

Requires a working install of NMAP present in user's path.

Usage:

First, generate a database object:
    `$ python3 register.py "Ariana Giroux" "Arianas-IDENTIFIER"`
For more information on generating database objects:
    `$ python3 register.py -h`

Then, to run the UserChecker interface do the following:
    >>> from core import Loader
    >>> from core import generate_nmap
    >>> from core import UserChecker
    >>> db = Loader().load()
    >>> generate_nmap().wait()  # Run NMAP scan
    >>> # Parse nmap output enforcing connection confirmation polices, call callback on confirm
    >>> u = UserChecker(Loader().load(), lambda x: print('callback'))
    >>> for person in u:
    ... print(person.name)
    Ariana
    callback
"""
import subprocess
import time
from tempfile import NamedTemporaryFile
import os

from . import Loader, DB_PATH
from .log import logger

# CONSTANTS
CONNECTION_CONFIRM = 1200  # 20 minutes in seconds
DISCONNECTION_CONFIRM = 3600  # 1 hour in seconds
ERR_FILE = NamedTemporaryFile('a+')
OUT_FILE = NamedTemporaryFile('a+')


class UserChecker:
    """ Implements output search functionality, enforcing connection polices. """
    def __init__(self, db, func, quiet=False, output_file=OUT_FILE):
        """ Initializes variables that must be accessible.

        `db` = A database object loaded by Loader.load.
        `func` = The callback function.
        `quiet` = Verbosity flag.
        `output_file` = The file to check for user connectivity.
        """

        self.func = func
        self.db = db
        self.quiet = quiet
        self.output_file = OUT_FILE

    def grep_output(self, term, output_file=OUT_FILE, quiet=False):
        """ Parses `output_file` for the appearance of term. Returns `True` if found. """

        for line in output_file:
            logger.debug(str(line).strip('\n'))
            if line.count(term):
                logger.debug('%s present' % term)
                return True

        else:
            logger.debug('%s not present' % term)
            return False

    def announce(self, person):
        """ Calls `self.func` (the callback function), passing it a `data.Person`
        object. """
        self.func(person)

    def check_for_people(self, db, quiet):
        """ For each person in `db`, update the person's fields based on connection policies. """
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

                        if not quiet:
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
                                    CONNECTION_CONFIRM and not \
                                    person.connection_announced:

                                person.connection_announced = True
                                self.announce(person)

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

                    if not quiet and person.is_connected:
                        # Only output data to the stream if they were previously
                        # connected
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
                                DISCONNECTION_CONFIRM and not \
                                person.disconnection_announced:
                            person.disconnection_announced = True
                            self.announce(person)
                            person.connection_started = 0.0

                    yield person

    def __iter__(self):
        """ Provides an easy interface to run the search. Yields each person from
        `self.check_for_people`. """
        for person in self.check_for_people(self.db, self.quiet):
            yield person


def reset(db):
    """ Resets all data fields in `db`. Assumes `db` is `data.Database.version == 1`.

    Also resets `global OUT_FILE` and `global OUT_FILE`
    """
    db = Loader().load()  # DEBUG Why is this here? Overrides `db` arg
    for person in db.yield_people():
        person.is_connected = False
        person.last_connected = 0.0
        person.connection_started = 0.0
        person.connection_announced = False
        person.disconnection_announced = False
    Loader().dump(db)

    ERR_FILE.truncate(0)
    OUT_FILE.truncate(0)


def generate_nmap(output_file=OUT_FILE, ip_range='192.168.1.0/24',
                  script_path=None):
    """ Returns a subprocess.Popen object running an NMAP request. Optionally,
    the user can supply a script path for custom results. Outputs all results
    to `output_file.`

    `output_file` - The file to write `subprocess.Popen` output to.
        Defaults to `global OUT_FILE`
    `ip_range` - The IP range to scan. Defaults to `192.168.1.0/24`.
        If `script_path` is specified, this kwarg does not get used.
    `script_path` - The path to a user specified script.
        The script must output any useful information to STDOUT. The script must
        also be able to be executed by this scripts UID.

    `returns` - A `subprocess.Popen` object.
    """

    with open(output_file.name, 'w') as outfile:
        outfile.truncate(0)

    if script_path is None:
        return subprocess.Popen(['nmap', '-sP', ip_range], stdout=output_file,
                                stderr=ERR_FILE)
    elif os.access(script_path, os.F_OK):
        return subprocess.Popen(script_path, stdout=output_file,
                                stderr=ERR_FILE)


if __name__ == '__main__':
    DeprecationWarning('Direct execution of core has been deprecated! Use '
                       'main.py')
