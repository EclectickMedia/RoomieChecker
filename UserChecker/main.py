""" Implements an `argparse.ArgumentParser` based interface for the package.
Does not provide any useful code access points.
Parser Usage:
usage: main.py [-h] [-d DELAY] [-q] [-r IPRANGE] [-R]

optional arguments:
  -h, --help            show this help message and exit
  -d DELAY, --delay DELAY
                        The amount of time (in seconds) to delay between each
                        NMAP scan. Defaults to 0 (instant)
  -q, --quiet           Do not output to STDOUT
  -r IPRANGE, --iprange IPRANGE
                        The IP range to attempt to scan. Defaults to
                        '192.168.1.0/24'
  -R, --reset           Reset the on line status of the users in the database
"""

import argparse
import sys
import time
import os

from . import Loader
from .core import ERR_FILE, OUT_FILE, reset, generate_nmap, UserChecker
from .log import logger


l = Loader()


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--delay',
                    help='The amount of time (in seconds) to delay between '
                    'each NMAP scan. Defaults to 0 (instant)', default=0,
                    type=int)
parser.add_argument('-q', '--quiet', help='Do not output to STDOUT',
                    action='store_true')

parser.add_argument('-r', '--iprange', help='The IP range to attempt to '
                    'scan. Defaults to \'192.168.1.0/24\'',
                    type=str, default='192.168.1.0/24')

parser.add_argument('-R', '--reset', help='Reset the on line status of the'
                    ' users in the database', action='store_true')


def run():
    parsed = parser.parse_args()

    if parsed.reset:
        reset(l.load())
        exit()

    start_time = time.time()
    logger.debug("runtime start")
    while 1:
        # Clear OUT_FILE
        OUT_FILE.truncate(0)

        if not parsed.quiet:
            logger.info('Refreshing DB')

        # Load a db
        db = l.load()
        logger.debug('Loaded DB: %s' % str(db))
        if not parsed.quiet:
            logger.info('Running NMAP to find connected devices.')

        # Generate an NMAP object, and wait for it to finish its scan
        logger.debug('Generate NMAP scan, wait')
        generate_nmap(OUT_FILE, parsed.iprange).wait()

        def callback(person):
            print('got %s' % person.name)

        for person in UserChecker(db, callback, quiet=parsed.quiet):
            pass

        if (time.time() - start_time) > 1200:  # TODO what is this doing here?
            ERR_FILE.truncate(0)
            start_time = time.time()

        l.dump(db)  # Dump db back to disk

        if time.time() - start_time > 120 and not sys.argv.count('-q'):
            os.system('cls' if os.name == 'nt' else 'clear')
            start_time = time.time()

        time.sleep(parsed.delay)


if __name__ == '__main__':
    run()

    raise DeprecationWarning('Direct execution of main.py will soon be deprecated.')
