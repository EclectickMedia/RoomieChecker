import argparse
import sys
import time
from platform import system
from tempfile import NamedTemporaryFile

import core

l = core.Loader()
ERR_FILE = NamedTemporaryFile('a+')
OUT_FILE = NamedTemporaryFile('a+')
DB_PATH = 'db.pkl'


parser = argparse.ArgumentParser()
parser.add_argument('-q', '--quiet', help='Do not output to STDOUT',
                    action='store_true')

parser.add_argument('-r', '--iprange', help='The IP range to attempt to '
                    'scan.', type=str)

parser.add_argument('-R', '--reset', help='Reset the on line status of the'
                    ' users in the database', action='store_true')

parsed = parser.parse_args()

if parsed.reset:
    core.reset(l.load())
    exit()

start_time = time.time()
while 1:
    OUT_FILE.truncate(0)

    if not parsed.quiet:
        print('Refreshing DB')

    db = l.load()

    if not parsed.quiet:
        print('Running NMAP to find connected devices.')

    if parsed.iprange is None:
        core.generate_nmap(OUT_FILE).wait()
    else:
        core.generate_nmap(OUT_FILE, ip_range=parsed.iprange).wait()

    for person in core.check_for_people(db, parsed.quiet):
        core.announce(person)

    if (time.time() - start_time) > 1200:
        ERR_FILE.truncate(0)
        start_time = time.time()

    # time.sleep(10)
    l.dump(db)

    if not sys.argv.count('-q'):
        system('clear')