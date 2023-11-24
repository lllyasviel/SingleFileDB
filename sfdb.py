# Single File Database
# Written by Lvmin Zhang
# 2022 Dec 23 at Stanford University

import sys
import json
import time
import sqlite3
import datetime
import threading


def now():
    return datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")


def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class Database:
    def __init__(self, filename, read_only=False):
        self._filename = filename
        if read_only:
            self._sqlite = sqlite3.connect(f'file:{self._filename}?mode=ro', check_same_thread=False, uri=True)
        else:
            self._sqlite = sqlite3.connect(self._filename, check_same_thread=False)
        self._sqlite.execute("CREATE TABLE IF NOT EXISTS DATA(ID TEXT NOT NULL UNIQUE, TIME TEXT NOT NULL, JSON TEXT NOT NULL, PRIMARY KEY (ID))")
        self._sqlite.commit()
        self._lock = threading.Lock()
        self._iterating = False
        self._commit_timer = time.time()
        self._commit_counter = 0
        log(f'SFDB[{self._filename}] Database ready with {len(self)} rows.')

    def _sanity_check(self):
        assert self._sqlite is not None, f'SFDB[{self._filename}] Database already closed.'
        assert not self._iterating, f'SFDB[{self._filename}] Database cannot be accessed inside an iterating loop.'

    def _key_is_str(self, key):
        assert isinstance(key, str), f'SFDB[{self._filename}] All keys must be str, get \"{type(key).__name__}\" instead.'

    def __len__(self):
        self._sanity_check()
        with self._lock:
            x = self._sqlite.execute("SELECT COUNT(ID) FROM DATA").fetchone()
            return x[0] if x is not None else 0

    def __getitem__(self, key):
        self._sanity_check()
        self._key_is_str(key)
        with self._lock:
            item = self._sqlite.execute("SELECT JSON FROM DATA WHERE ID = ?", (key,)).fetchone()
        if item is None:
            raise KeyError(key)
        return json.loads(item[0])

    def get(self, key, default=None):
        self._sanity_check()
        self._key_is_str(key)
        with self._lock:
            item = self._sqlite.execute("SELECT JSON FROM DATA WHERE ID = ?", (key,)).fetchone()
        return json.loads(item[0]) if item is not None else default

    def __contains__(self, key):
        self._sanity_check()
        self._key_is_str(key)
        with self._lock:
            return self._sqlite.execute("SELECT 1 FROM DATA WHERE ID = ?", (key,)).fetchone() is not None

    def __setitem__(self, key, value):
        self._sanity_check()
        self._key_is_str(key)
        feed = (key, now(), json.dumps(value))
        with self._lock:
            self._sqlite.execute("INSERT OR REPLACE INTO DATA(ID, TIME, JSON) VALUES(?, ?, ?)", feed)
            self._commit_counter += 1
        self._auto_commit()
        return

    def __delitem__(self, key):
        self._sanity_check()
        self._key_is_str(key)
        with self._lock:
            self._sqlite.execute("DELETE FROM DATA WHERE ID = ?", (key,))
            self._commit_counter += 1
        self._auto_commit()
        return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return

    def __del__(self):
        self.close()
        return

    def _auto_commit(self):
        if time.time() > self._commit_timer + 60 or self._commit_counter > 1024 * 16:
            self.commit()
        return

    def commit(self):
        self._sanity_check()
        with self._lock:
            self._sqlite.commit()
            log(f'SFDB[{self._filename}] Committed {self._commit_counter} transactions during the last {"%.2f" % (time.time() - self._commit_timer)} seconds.')
            self._commit_timer = time.time()
            self._commit_counter = 0
        return

    def close(self):
        if self._sqlite is None:
            return
        self._sanity_check()
        self.commit()
        with self._lock:
            self._sqlite.close()
            self._sqlite = None
            log(f'SFDB[{self._filename}] Database connection closed.')
        return

    def __iter__(self):
        self._sanity_check()
        with self._lock:
            try:
                self._iterating = True
                for item in self._sqlite.execute('SELECT ID, JSON FROM DATA'):
                    yield item[0], json.loads(item[1])
            finally:
                self._iterating = False

    def keys(self):
        self._sanity_check()
        with self._lock:
            return [x[0] for x in self._sqlite.execute('SELECT ID FROM DATA').fetchall()]

    def todict(self):
        self._sanity_check()
        with self._lock:
            return {x[0]: json.loads(x[1]) for x in self._sqlite.execute('SELECT ID, JSON FROM DATA').fetchall()}

    def tolist(self):
        self._sanity_check()
        with self._lock:
            return [(x[0], json.loads(x[1])) for x in self._sqlite.execute('SELECT ID, JSON FROM DATA').fetchall()]

