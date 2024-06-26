#!/usr/bin/python3
"""
User Module: The definition, documentation and encapsulation
of all common attributes and methods for the User class
"""
from importlib import import_module


models = import_module("models")


class User(models.BaseModel):
    """
    The definition, documentation and encapsulation of all common
    attributes and methods for the User class
    """

    def __init__(self, *args, **kwargs):
        """
        Initialises attributes to empty strings if not kwargs
        provided, else passes initialisation on to the the
        parent
        """

        self.first_name = self.last_name = ""
        self.email = self.password = ""
        super().__init__(*args, **kwargs)
