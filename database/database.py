import logging
import threading
import sqlite3
import os

CURRENT_DIRPATH = os.path.dirname(__file__)
TABLES_PATH = os.path.join(CURRENT_DIRPATH, "tables.sql")
DATABASE_PATH = os.path.join(CURRENT_DIRPATH, "data.db")


class Database:
    lock = threading.Lock()
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = true;")
    with open(TABLES_PATH) as f:
        cursor.executescript(f.read())

    def __enter__(self):
        self.lock.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.lock.release()

    def insert(self, sql: str, **kwargs):
        try:
            self.cursor.execute(sql, kwargs)
            return self.cursor.lastrowid
        except Exception as e:
            logger.debug(sql, kwargs)
            logger.exception(e)
            raise

    def select(self, sql: str, **kwargs):
        try:
            self.cursor.execute(sql, kwargs)
            return self.cursor.fetchall()
        except Exception as e:
            logger.debug(sql, kwargs)
            logger.exception(e)
            raise

    def update(self, sql: str, **kwargs):
        try:
            self.cursor.execute(sql, kwargs)
        except Exception as e:
            logger.debug(sql, kwargs)
            logger.exception(e)
            raise

    def delete(self, sql: str, **kwargs):
        try:
            self.cursor.execute(sql, kwargs)
        except Exception as e:
            logger.debug(sql, kwargs)
            logger.exception(e)
            raise


LOG_DIRPATH = "../log"
LOG_NAME = os.path.splitext(os.path.split(__file__)[1])[0]
os.makedirs(os.path.join(CURRENT_DIRPATH, LOG_DIRPATH), exist_ok=True)
filepath = os.path.join(CURRENT_DIRPATH, LOG_DIRPATH, F"{LOG_NAME}.log")
LOG_FORMAT = "%(asctime)s - %(levelname)s :: %(name)s %(lineno)d :: %(message)s"
logger = logging.getLogger(LOG_NAME)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(filepath, "w", encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(fh)
logger.propagate = False
