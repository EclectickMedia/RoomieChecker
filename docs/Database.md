# Database Preamble

The 'database' used by this software is in no way a database.

It is instead just a python `list` object with embedded `dict` objects that has
been serialized by python's [pickle][1] module.

---

# Database Structure

The database is constructed as follows:
```python
[
    {
        'name': 'User\'s Name',
        'ident': 'User\'s unique network identifier',
        'is_connected': False  # True if the user is connected to the network.
    },
    {
        'name': 'Second User\'s Name',
        'ident': 'Second User\'s unique network identifier',
        'is_connected': False  # True if the user is connected to the network.
    }
]
```

The actual user data is contained within `dict` objects with the following
fields:
1. A `name` field
   - The user's actual name.
2. A unique identifier field called `ident`
   - The unique identifier that their machine provides the network, visible by
     NMAP.
3. A field to track user connectivity called `is_connected`
   - Stores `False` if the user is not connected, or `True` if they are
     currently connected.
