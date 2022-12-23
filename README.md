# Single File Database (SFDB)

A single file implementation of key-value database for Python 3.

I use this to store millions of image metadata in many machine learning projects. 

It is very useful. 

# Installation

**Just copy the single file "sfdb.py" to any project.**

No installation. No dependencies. 

The [only one python file](https://github.com/lllyasviel/SingleFileDB/blob/main/sfdb.py) has **less than 150 lines of codes** and only uses Python 3 standard libraries.

# Just try this

```python
import sfdb

db = sfdb.Database(filename='test.db')  # Will create a new file or open an existing file.

# Add or update items
db['hello'] = 1
db['123'] = 'hi'
db['a'] = [1, 2, 3]
db['bad'] = 'garbage'

# Delete items
del db['bad']

# Read items
print(db['123'])  # Will print "hi".
```

# And you will immediately get

### 1. Human-Readable Storage

Your data is stored with sqlite format, so that you can view all your data with any sqlite viewers like [SQLiteStudio](https://sqlitestudio.pl/) or [Jetbrain Datagrip](https://www.jetbrains.com/datagrip/).

All items are human-readable json text. 

You can access all data even without using SFDB.

View (and even edit) your data anytime outside your project.

![a1](https://raw.githubusercontent.com/lllyasviel/lllyasviel.github.io/master/db.jpg)

This is what you see in your file explorer:

![a2](https://raw.githubusercontent.com/lllyasviel/lllyasviel.github.io/master/f.jpg)

### 2. Fast Access from Memory

If your database is small, you can just read everything to memory to various format with one line of code.

```python
import sfdb

db = sfdb.Database(filename='test.db')

cache = db.tolist()
print(cache)
# [('hello', 1), ('123', 'hi'), ('a', [1, 2, 3])]

cache = db.todict()
print(cache)
# {'hello': 1, '123': 'hi', 'a': [1, 2, 3]}

cache = db.keys()
print(cache)
# ['123', 'a', 'hello']
```

### 3. Process 10TB Data with 10MB Memory

You can process any large data without loading everything to your memory.

```python
import sfdb

db = sfdb.Database(filename='very_large_database_with_10TB.db')  # Oh god this database has 10 TB data.

db['anything'] = 123456  # Update it without loading database to memory.

if 'another_thing' in db:
    print('Cool!')  # Search item without loading database to memory.

# Get item
print(db['another_thing'])  

# Try to get item with default value as None if item not found.
print(db.get('another_thing', default=None))

for key, value in db:
    # Read data items one-by-one. This only requires very small memory.
    print(key)
    print(value)
```

### 4. Thread-Safe Everything

Everything is thread-safe. 

Do anything you want to do. 

Your data are safe.

### 5. Reliable Storage and Automatic Damage Repair

All data are valid if you only write valid data.

Quit you application with Ctrl+C does not damage the integrity of database structure.

A reference is [here](https://www.sqlite.org/howtocorrupt.html):

    An SQLite database is highly resistant to corruption. If an application crash, 
    or an operating-system crash, or even a power failure occurs in the middle of a 
    transaction, the partially written transaction should be automatically rolled 
    back the next time the database file is accessed. The recovery process is fully 
    automatic and does not require any action on the part of the user or the application.

### 6. Minimal Hard Disk Write

The hard disk writing is optimized to speed up the processing and protect your SSD/HDD drive.

All data updating are updated immediately from the perspective of your python program (*i.e.*, your code logic), but the actual writing to the hard disk only happens when 

(1) your program quit, **OR**

(2) every 16384 (16 * 1024) updates, **OR**

(3) every 60 seconds.

You can force all updates to be written to the hard disk with

```python
db.commit() # But you do not need to do it.
```

but **you do NOT need** to do so, since it is slow, and we have already optimized it. Or you can use

```python
db.close()  # Close a database when you quit (but you do not need to do it).
```

or

```python
del db  # Dispose the instance when you quit (but you do not need to do it).
```

### 7. Professional Language Feature Support

If you want to look professional, you can use "with" context manager like

```python
import sfdb

with sfdb.Database(filename='test.db') as db:
    print(db['hello'])
```

Or if you like "tqdm" you can use

```python
import sfdb
from tqdm import tqdm

db = sfdb.Database(filename='test.db')

for key, value in tqdm(db):
    # You will have a nice progress bar provided by tqdm.
    print(key)
    print(value)
```

# Licence

[CC-By 4.0](https://creativecommons.org/licenses/by/4.0/) - Do whatever you want to do.
