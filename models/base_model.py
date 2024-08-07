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

    __IMMUTABLES__ = ["id", "created_at", "updated_at"]

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
    def create(cls):
        """
        Creates a new instance of a model, saves the
        instance and prints the instance's id. BaseModel
        is not recognised as a valid model
        """

        if BaseModel.is_base_model(cls.__name__):
            return print("** model doesn't exist **")

        model = cls()
        model.save()
        print(model.id)

    @classmethod
    def count(cls):
        """Display number of all class specific instances in storage"""

        count = sum(
            model.get("__class__") == cls.__name__
            for model in models.storage.all().values()
        )

        print(f"{cls.__name__} count: {count}")

    @classmethod
    def destroy(cls, instance_id=None):
        """
        Deletes an instance of the model matching the
        given id. The user is informed should:
            - The model's name be missing or invalid
            - The model not exist
            - The id be missing or invalid
            - The id refer to a non-existing instance
        """

        if BaseModel.is_base_model(cls.__name__):
            return print("** model doesn't exist **")

        if not BaseModel.is_valid_id(instance_id):
            return

        key = f"{cls.__name__}.{instance_id}"
        models.storage.all().pop(key)
        models.storage.save()

    @classmethod
    def is_base_model(cls, model_name):
        return model_name.lower() in ["basemodel", cls.__name__.lower()]

    @classmethod
    def is_valid_id(cls, instance_id):
        """Validates instance id as being existant"""

        keys = models.storage.all().keys()
        elements = [element for key in keys for element in key.split(".")]

        if not instance_id:
            print("** instance id missing **")
            return False

        if instance_id not in elements:
            print("** no instance found **")
            return False

        return True

    @classmethod
    def is_valid_model(cls, model_name):
        """Validates model name as being existant"""

        if not model_name:
            print("** model name missing **")
            return False

        is_not_model = model_name not in models.ALL_MODELS
        is_base_model = BaseModel.is_base_model(model_name)

        if is_base_model or is_not_model:
            print("** model doesn't exist **")
            return False

        return True

    def save(self):
        """Saves present model to storage"""

        self.updated_at = datetime.now()
        models.storage.save()

    @classmethod
    def show(cls, instance_id=None):
        """
        Prints the string representation of an instance
        based on the model name and id. If the model name
        or id are missing, the user is informed.

        Parameter
        ---------
        instance_id: str
            id of instance

        Expected
        --------
            (anna) <model>.show(<id>)


        Missing Instance ID
        -------------------
            (anna) <model>.show()
            ** no instance found **
            (anna) <model>.show('')
            ** no instance found **

        Non-Existant Instance ID
        ------------------------
            (anna) <model>.show('123-456-789')
            ** no instance found **
        """

        if not BaseModel.is_valid_id(instance_id):
            return

        key = f"{cls.__name__}.{instance_id}"
        kwargs = models.storage.all().get(key)

        if not kwargs:
            return print("** no instance found **")

        Model = models.ALL_MODELS.get(cls.__name__)
        model = Model(**kwargs)

        print(model)

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
            key: value.isoformat() if isinstance(value, datetime) else value
            for key, value in sorted(self.__dict__.items())
        }

        return {
            "__class__": self.__class__.__name__,
            **dict_,
        }

    @classmethod
    def update(cls, instance_id=None, attribute=None, value=None):
        """
        Updates an instance of the model matching the
        given id. The updated instance is then sent to
        storage. One attribute can be updated at a time,
        whereby the attribute value is cast into one of
        three types: float, int or str

        Of note is that `id`, `created_at` and `updated_at`
        cannot be updated.
        """

        if BaseModel.is_base_model(cls.__name__):
            return print("** model doesn't exist **")

        if attribute in cls.__IMMUTABLES__:
            return print("** immutable attribute **")

        if not BaseModel.is_valid_id(instance_id):
            return

        if not attribute:
            return print("** attribute missing **")

        if not value:
            return print("** value missing **")

        key = f"{cls.__name__}.{instance_id}"
        kwargs = models.storage.all().get(key)

        if attribute:
            kwargs[attribute] = value

        model = cls(**kwargs)
        model.save()
        return model

    def __eq__(self, other):
        have_same_ids = self.super_id == other.super_id
        have_same_created_at = self.created_at == other.created_at
        return have_same_ids and have_same_created_at

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

        dict_ = {key: value for key, value in sorted(self.__dict__.items())}
        name = self.__class__.__name__
        return f"[{name}] ({self.id}) {dict_}"
