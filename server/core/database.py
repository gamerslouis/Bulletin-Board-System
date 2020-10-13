import sqlite3
import settings
import threading

__db__thread__objects__ = {}


def get_db() -> sqlite3.Connection:
    ident = threading.get_ident()
    if ident not in __db__thread__objects__:
        __db__thread__objects__[ident] = sqlite3.connect(settings.db_name)
    return __db__thread__objects__[ident]

def close_db():
    ident = threading.get_ident()
    if ident in __db__thread__objects__:
        __db__thread__objects__[ident].close()
        del __db__thread__objects__[ident]

class db__wrapper():
    def __getattr__(self, name):
        return getattr(get_db(), name)

    def __setattr__(self, name, value):
        setattrI(get_db(), name, value)


db = db__wrapper()
