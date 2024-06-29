#!/usr/bin/python3
"""
Review Module: The definition, documentation and encapsulation
of all common attributes and methods for the Review class
"""
from importlib import import_module


models = import_module("models")


class Review(models.BaseModel):
    """
    The definition, documentation and encapsulation of all common
    attributes and methods for the Review class
    """

    def __init__(self, *args, **kwargs):
        """
        Initialises attributes to empty strings if not kwargs
        provided, else passes initialisation on to the the
        parent
        """

        self.place_id = ""
        self.user_id = ""
        self.text = ""
        super().__init__(*args, **kwargs)
