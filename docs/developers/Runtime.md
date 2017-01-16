# Runtime Breakdown

The software is run by executing `$ python check_for_users.py`.

---

## Module load

Upon module load, the script imports all necessary softwares, and declares the
following global variables:

1. ERR_FILE (a `NamedTemporaryFile` object to store errors from the NMAP call.)
2. OUT_FILE (a `NamedTemporaryFile` object to store the output of the NMAP
   call.)
3. DB_PATH (a default path to attempt to load data from via [load db][3])

---

## Get program arguments:
Upon startup, the software checks for a series of command line arguments under
the following lines from [this file][1]:
```python
if __name__ == '__main__':
    ...
```

This block of code makes use of python's `argparse` library, which provides an
easy to understand command line argument interface. 

> Check out the [argparse docs][2] for a further explanation on how this module
> operates.

After registering, and parsing the arguments, this block of code passes the
arguments to `check_for_users.run`.

---

## The main runtime loop:

The software maintains a loop under the function `run` that executes all of the
main logic.

The loop runs the following order of operations:

1. Initialize a `start_time` via python's `time.time()`,
2. Enter an infinite while loop (`while 1:`),
3. Ensure that `OUT_FILE` has no data in it via `OUT_FILE.truncate`,
4. Executes [load db][3], storing the results in `db`,
5. Executes [generate nmap][4], which writes the results of an `nmap -sP` call
   to `OUT_FILE`
6. Executes [check for people][5], providing the database loaded into `db` and
   the verbosity flag (`quiet`)
7. If enough time has passed, ensures that `ERR_FILE` has no data, and sets the
   `start_time` to the current `time.time()` value.
8. Stores the currently modified database via [dump db][6]
9. If the script is executing with verbosity, clear the STDOUT via
   `system('clear')`
10. Start the loop again.

[1]: ../../check_for_users.py
[2]: https://docs.python.org/3/library/argparse.html
[3]: ../docs/developers/functions/load_db.md
[4]: ../docs/developers/functions/generate_nmap.md
[5]: ../docs/developers/functions/check_for_people.md
[6]: ../docs/developers/functions/dump_db.md
