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

    def __init__(self, *args, **kwargs):
        """
        Spawns an existing object or generates a new one

        Parameters
        ----------
        args : Any
            unused

        kwargs : Any
            keyword-to-value pairings used to deserialise
            and spawn existing objects
        """

        self.__init_kwargs__(kwargs) if kwargs else self.__init_default__()

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

    @property
    def updated_at(self):
        """
        Returns a datetime object representing the local time
        at which the model was last updated
        """

        return self.__updated_at

    def __init_default__(self):
        """Generates a new BaseModel object"""

        self.__id = str(uuid4())
        self.__created_at = self.__updated_at = datetime.now()

    def __init_kwargs__(self, kwargs):
        """
        Spawns an existing object

        Parameters
        ----------
        kwargs : Any
            keyword-to-value pairings used to deserialise
            and spawn existing objects
        """

        dt_attr = {"created_at": None, "updated_at": None}
        dt_format = "%Y-%m-%dT%H:%M:%S.%f"

        for attr, value in kwargs.items():

            if attr in dt_attr:
                value = datetime.strptime(value, dt_format)
                dt_attr[attr] = value
                continue

            elif attr.count("id"):
                self.__id = value
                continue

            self.__dict__[attr] = value

        self.__created_at = dt_attr.get("created_at")
        self.__updated_at = dt_attr.get("updated_at")

    def __setattr__(self, name, value):
        """
        Customised process when creating or updating an
        attribute, principally to update the `updated_at`
        attribute to the time of use

        Parameters
        ----------
        name : str
            the name of the attribute

        value : Any
            the value being assigned to the provided
            attribute
        """

        if name.count("updated_at"):
            return super().__setattr__(name, value)

        self.__updated_at = datetime.now()
        super().__setattr__(name, value)
