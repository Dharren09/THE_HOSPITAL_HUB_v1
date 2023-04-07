#!/usr/bin/python3
from os import getenv
storage_ENV = getenv("STORAGE_ENV")

if storage_ENV == "db":
    from models.engine.db_storage import DB_Storage
    storage = DB_Storage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
