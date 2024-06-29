#!/usr/bin/python3
"""
City Module: The definition, documentation and encapsulation
of all common attributes and methods for the City class
"""
from importlib import import_module


models = import_module("models")


class City(models.BaseModel):
    """
    The definition, documentation and encapsulation of all common
    attributes and methods for the City class
    """

    def __init__(self, *args, **kwargs):
        """
        Initialises attributes to empty strings if not kwargs
        provided, else passes initialisation on to the the
        parent
        """

        self.name = ""
        self.state_id = ""
        super().__init__(*args, **kwargs)
