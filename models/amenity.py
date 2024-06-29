#!/usr/bin/python3
"""
Amenity Module: The definition, documentation and encapsulation
of all common attributes and methods for the Amenity class
"""
from importlib import import_module


models = import_module("models")


class Amenity(models.BaseModel):
    """
    The definition, documentation and encapsulation of all common
    attributes and methods for the Amenity class
    """

    def __init__(self, *args, **kwargs):
        """
        Initialises attributes to empty strings if not kwargs
        provided, else passes initialisation on to the the
        parent
        """

        self.name = ""
        super().__init__(*args, **kwargs)
