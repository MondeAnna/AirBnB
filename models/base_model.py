#!/usr/bin/python3
"""
Base Module: Definition, documentation and encapsulation of
all common attributes and methods for the project's classes
"""


from importlib import import_module
from datetime import datetime
import uuid


models = import_module("models")


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
        models.storage.new(self)

    @classmethod
    def all(cls):
        """
        Prints a list of string representations of all instances.
        Where instances are scoped to calling class.
        """

        all_super_ids = [
            model for model in models.storage.all().keys()
            if model.count(cls.__name__)
        ]

        for super_id in all_super_ids:
            print(super_id)

    @classmethod
    def count(cls):
        """Display number of all class specific instances in storage"""

        count = sum(
            model.get("__class__") == cls.__name__
            for model in models.storage.all().values()
        )

        print(f"{cls.__name__} count: {count}")

    def save(self):
        """Saves present model to storage"""

        self.updated_at = datetime.now()
        models.storage.save()

    @property
    def super_id(self):
        """
        Returns the model's name prepended to its version four
        form of the RFC 4122 Standardised UUID (Universally Unique
        Identifiers)
        """

        return f"{self.__class__.__name__}.{self.id}"

    def to_dict(self):
        """
        Returns serialised method/attr-to-value pair for current
        model
        """

        dict_ = {
            key: value.isoformat()
            if isinstance(value, datetime) else value
            for key, value in sorted(self.__dict__.items())
        }

        return {
            "__class__": self.__class__.__name__,
            **dict_,
        }

    def __init_default__(self):
        """Generates a new BaseModel object"""

        self.id = str(uuid.uuid4())
        self.created_at = self.updated_at = datetime.now()

    def __init_kwargs__(self, kwargs):
        """
        Spawns an existing object

        Parameters
        ----------
        kwargs : Any
            keyword-to-value pairings used to deserialise
            and spawn existing objects
        """

        dt_attr = ["created_at", "updated_at"]

        for attr, value in kwargs.items():

            if attr in dt_attr:
                format = "%Y-%m-%dT%H:%M:%S.%f"
                value = datetime.strptime(value, format)

            self.__dict__[attr] = value

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
        self.__dict__["updated_at"] = datetime.now()
        super().__setattr__(name, value)

    def __str__(self):
        """Returns a string representing the current model"""

        dict_ = {
            key: value
            for key, value in sorted(self.__dict__.items())
        }

        name = self.__class__.__name__
        return f"[{name}] ({self.id}) {dict_}"
