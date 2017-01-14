# Function Logic

The function parses through the database object (described in detail [here][1])
and checks to see if each user's unique network identifier was visible to NMAP.

It operates in the following order:

1. Get a person from the database
   - Each person is represented by one of the embedded dicts detailed [here][1]
2. Obtain a readable file stream from `OUT_FILE`.
   - `OUT_FILE` is initiated as writable, so we need to obtain the stream again
     as a readable object.
3. Check if [grep output][2] returns positive for the current user.
   - If the users identifier was found, and if the user is not currently
     connected:
     
     1. Set the person's `is_connected` field to `True`.
     2. Execute the announcer function.

   - If the users identifier was not found, and the user's `is_connected` field
     is currently set to `True`:

     1. Execute the announcer function, announcing user disconnection.
     2. Set the user's `is_connected` field to false.
4. Loop

---

# Function parameters:

1. db
   A database object loaded via [load db][3]
2. quiet
   The verbosity flag obtained via `argparse`.

[1]: ../../docs/Database.md
[2]: ../docs/functions/grep_output.md
[3]: ../docs/functions/load_db.md
