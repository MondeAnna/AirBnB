#!/usr/bin/python3
"""Pre-Initial vital system components"""


from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
