#!/usr/bin/python3
"""
File Storage: Definition, documentation and encapsulation
of all models onto the operating system's file storage
"""


from datetime import datetime
import uuid


class FileStorage:
    """
    Definition, documentation and encapsulation of all
    models onto the operating system's file storage
    """

    __file_path = ""
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
