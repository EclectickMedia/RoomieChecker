import argparse
import sys
import time
import os

import core
from core import ERR_FILE, OUT_FILE
from log import logger

l = core.Loader()


parser = argparse.ArgumentParser()
parser.add_argument('-q', '--quiet', help='Do not output to STDOUT',
                    action='store_true')

parser.add_argument('-r', '--iprange', help='The IP range to attempt to '
                    'scan. Defaults to \'192.168.1.0/24\'',
                    type=str, default='192.168.1.0/24')

parser.add_argument('-R', '--reset', help='Reset the on line status of the'
                    ' users in the database', action='store_true')

parsed = parser.parse_args()

if parsed.reset:
    core.reset(l.load())
    exit()

start_time = time.time()
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
    core.generate_nmap(OUT_FILE, parsed.iprange).wait()

    for person in core.check_for_people(db, parsed.quiet):
        core.announce(person.name)

    if (time.time() - start_time) > 1200:  # TODO what is this doing here?
        ERR_FILE.truncate(0)
        start_time = time.time()

    l.dump(db)  # Dump db back to disk

    if time.time() - start_time > 120 and not sys.argv.count('-q'):
        os.system('cls' if os.name == 'nt' else 'clear')
        start_time = time.time()
