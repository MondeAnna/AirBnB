#!/usr/bin/python3
"""
File Storage: Definition, documentation and encapsulation
of all models onto the operating system's file storage
"""
from datetime import datetime
from pathlib import Path
import json
import uuid


class FileStorage:
    """
    Definition, documentation and encapsulation of all
    models onto the operating system's file storage
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Provides all models in storage"""

        return self.__objects

    def new(self, model):
        """
        Updates cached items with the retrieval
        key of <model class name>.id

        Parameter
        ---------
        model : BaseModel | subclass(BaseModel)
            model to be tracked
        """

        self.__objects[model.super_id] = model.to_dict()

    def reload(self):
        """Reload cache with models stored on file"""

        path = Path(self.__file_path)

        if not path.is_file():
            return

        if not path.stat().st_size:
            self.__objects = {}
            return

        with open(self.__file_path, "r") as file:
            self.__objects = json.load(file)

    def save(self):
        """
        Writes to file cached models as JSON
        Serialised values
        """

        path = Path(self.__file_path)

        if not path.is_file():
            path.touch()

        with open(self.__file_path, "w") as file:
            json.dump(self.__objects, file)
