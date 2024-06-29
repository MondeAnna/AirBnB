#!/usr/bin/python3
"""
State Module: The definition, documentation and encapsulation
of all common attributes and methods for the State class
"""
from importlib import import_module


models = import_module("models")


class State(models.BaseModel):
    """
    The definition, documentation and encapsulation of all common
    attributes and methods for the State class
    """

    def __init__(self, *args, **kwargs):
        """
        Initialises attributes to empty strings if not kwargs
        provided, else passes initialisation on to the the
        parent
        """

        self.name = ""
        super().__init__(*args, **kwargs)
