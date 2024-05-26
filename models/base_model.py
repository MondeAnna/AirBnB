#!/usr/bin/python3
"""
Base Module: Definition, documentation and encapsulation of
all common attributes and methods for the project's classes
"""


from datetime import datetime
from uuid import uuid4


class BaseModel:
    """
    Definition, documentation and encapsulation of all common
    attributes and methods for the project's classes
    """

    def __init__(self):
        self.__created_at = datetime.now()
        self.__id = str(uuid4())

    @property
    def id(self):
        """
        Returns the model's version four form of the RFC 4122
        Standardised UUID (Universally Unique Identifiers)
        """

        return self.__id

    @property
    def created_at(self):
        """
        Returns a datetime object representing the local time
        at which the model was first created
        """

        return self.__created_at
