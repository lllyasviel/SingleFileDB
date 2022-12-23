# Single File Database (SFDB)

A single file implementation of key-value database for Python 3.

I use this to store millions of image metadata in many machine learning projects. 

It is very useful. 

# Installation

**Just copy the single file "sfdb.py" to any project.**

No installation. No dependencies. 

The only one python file has less than 150 lines of codes and only uses Python 3 standard libraries.

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

![example](https://raw.githubusercontent.com/lllyasviel/lllyasviel.github.io/master/db.jpg)

### 2. Fast Access from Memory

123

### 3. Everything Thread-Safe

123

### 4. Process 10TB Data with 10MB Memory

123

### 5. Reliable Storage and Automatic Damage Repair

123

### 6. Minimal Hard Disk Write

123

### 7. Professional Language Feature Support

123

# Licence

[CC-By 4.0](https://creativecommons.org/licenses/by/4.0/) - Do whatever you want to do.
