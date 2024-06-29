#!/usr/bin/python3
"""CLI Backend Console"""
from collections import OrderedDict
from importlib import import_module
import shlex
import cmd


from models import *


class Console(cmd.Cmd):
    """CLI Backend Console"""

    prompt = "(anna) "

    def default(self, line):
        """
        Attempt at executing cli input when provided command
        does not match the provided definitions, where code
        is executed as though it is Python code

        Parameter
        ---------
        line : str
            user input

        Example
        -------
            (anna) User.all()
            User.0aff3461-4768-4d00-9a2e-0d58ce3e4a58
        """

        if "basemodel" in line.lower():
            return print(f"** unknown syntax: {line} **")

        try:
            exec(line)
        except Exception:
            print(f"** unknown syntax: {line} **")

    def do_all(self, model_name):
        """
        Prints a list of string representations of all model
        instances. Where model name is provided, models are
        scoped to said model. Where no model name is provided,
        all instance representations are printed.

        Parameter
        ---------
        model_name : str
            name of model to be represented

        Expected
        --------
            (anna) all
            (anna) all <model>
            <model>.<id>

        Non-Existant Model
        ------------------
            (anna) all DoesNotExist
            ** model doesn't exist **
        """

        is_not_model = model_name and model_name not in ALL_MODELS
        is_base_model = BaseModel.is_base_model(model_name)

        if is_base_model or is_not_model:
            return print("** model doesn't exist **")

        if not model_name:
            for cls in ALL_MODELS.values():
                cls.all()
        else:
            cls = ALL_MODELS.get(model_name)
            cls.all()

    def do_create(self, model_name):
        """
        Creates a new instance of a model, saves the instance and
        prints the instance's id. The user is informed should:
            - The model's name be missing or invalid
            - The model not exist

        Parameter
        ---------
        model_name : str
            name of model to create

        Expected
        --------
            (anna) create <model>
            <id>

        Missing Model Name
        ------------------
            (anna) create
            ** model name missing **

        Non-Existant Model
        ------------------
            (anna) create DoesNotExist
            ** model doesn't exist **
        """

        if not BaseModel.is_valid_model(model_name):
            return

        Model = ALL_MODELS.get(model_name)
        model = Model()
        model.save()
        print(model.id)

    def do_destroy(self, line):
        """
        Deletes an instance based on the model name and id
        with the changes saved to storage. The user is
        informed should:
            - The model's name be missing or invalid
            - The model not exist
            - The id be missing or invalid
            - The id refer to a non-existing instance

        Expected
        --------
            (anna) destroy <model> <id>

        Missing Model Name
        ------------------
            (anna) destroy
            ** model name missing **

        Non-Existant Model
        ------------------
            (anna) destroy DoesNotExist
            ** model doesn't exist **

        Missing Instance ID
        -------------------
            (anna) destroy <model>
            ** instance id missing **

        Non-Existant Instance ID
        ------------------------
            (anna) destroy <model> <id>
            ** no instance found **
        """

        parsed = self.__parse_line__(line)

        if not BaseModel.is_valid_model(parsed.get("model_name")):
            return

        if not BaseModel.is_valid_id(parsed.get("instance_id")):
            return

        key = f"{parsed.get('model_name')}.{parsed.get('instance_id')}"
        storage.all().pop(key)
        storage.save()

    def do_EOF(self, line):
        """Exits the programme when user enters `ctrl+d`"""

        print()
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""

        return True

    def do_show(self, line):
        """
        Prints the string representation of an instance
        based on the model name and id. The user is informed
        should:
            - The model's name be missing or invalid
            - The model not exist
            - The id be missing or invalid
            - The id refer to a non-existing instance

        Parameter
        ---------
        line : str
            user input expected to be two part expression
            containing

            model_name : str
                name of model to create

            instance_id : str
                id of instance

        Expected
        --------
            (anna) show <model> <id>
            <model-details>

        Missing Model Name
        ------------------
            (anna) show
            ** model name missing **

        Non-Existant Model
        ------------------
            (anna) show DoesNotExist
            ** model doesn't exist **

        Missing Instance ID
        -------------------
            (anna) show <model>
            ** instance id missing **

        Non-Existant Instance ID
        ------------------------
            (anna) show <model> <id>
            ** no instance found **
        """

        parsed = self.__parse_line__(line)

        if not BaseModel.is_valid_model(parsed.get("model_name")):
            return

        if not BaseModel.is_valid_id(parsed.get("instance_id")):
            return

        Model = ALL_MODELS.get(parsed.get("model_name"))
        Model.show(parsed.get("instance_id"))

    def do_update(self, line):
        """
        Updates an instance based on the model name and id
        by adding or updating attribute, which is then sent
        to storage. One attribute can be updated at a time,
        whereby the attribute value is cast into one of
        three type, float, int or str.

        N.B.: It is advise to input the attribute value within
        quotations

        Of note is that `id`, `created_at` and `updated_at`
        cannot be updated.

        Usage
        -----
            update <model name> <id> <attribute name> "<attribute value>"

        Expected
        --------
            (anna) update User 1234-1234-1234 email "aibnb@mail.com"

        Missing Model Name
        ------------------
            (anna) update
            ** model name missing **

        Non-Existant Model
        ------------------
            (anna) update DoesNotExist
            ** model doesn't exist **

        Missing Instance ID
        -------------------
            (anna) update Amenity
            ** instance id missing **

        Non-Existant Instance ID
        ------------------------
            (anna) update Place 123-456-789
            ** no instance found **

        Missing Attribute Name
        ----------------------
            (anna) update Review 123-456-789
            ** attribute name missing **

        Immutable Attributes
        --------------------
            (anna) update State created_at
            ** immutable attribute **

        Non-Existant Attribute Value
        ----------------------------
            (anna) update User 123-456-789 first_name
            ** value missing **
        """

        parsed = self.__parse_line__(line)

        if not BaseModel.is_valid_model(parsed.get("model_name")):
            return

        if not BaseModel.is_valid_id(parsed.get("instance_id")):
            return

        if not parsed.get("attribute"):
            return print("** attribute name missing **")

        immutables = ["id", "created_at", "updated_at"]
        if parsed.get("attribute") in immutables:
            return print("** immutable attribute **")

        if not parsed.get("value"):
            return print("** value missing **")

        key = f"{parsed.get('model_name')}.{parsed.get('instance_id')}"
        kwargs = storage.all().get(key)

        if parsed.get("attribute"):
            attr = parsed.get("attribute")
            kwargs[attr] = parsed.get("value")

        Model = ALL_MODELS.get(parsed.get("model_name"))
        Model(**kwargs).save()

    def emptyline(self):
        """Skips to new prompt should input be empty"""

        pass

    def __parse_line__(self, line):
        """
        Separate line into model name and instance id

        Parameter
        ---------
        line : str
            user provided input

        Return
        ------
        tuple[str]
            a paired tuple containing strings representing
            at index 0, the model name and at index 1,
            the instance id
        """

        parsed = OrderedDict(
            {
                "model_name": None,
                "instance_id": None,
                "attribute": None,
                "value": None,
            }
        )

        split = shlex.split(line)

        for key, value in zip(parsed, split):
            parsed[key] = value

        parsed["value"] = self.__type_value__(parsed.get("value"))

        return parsed

    @staticmethod
    def __type_value__(value):
        """
        Set the type of the value, at present limited to
        `float`, `int` and `str`

        Parameter
        ---------
        value : str
            user provided input

        Return
        ------
        float | int | str
            typed input from user
        """

        if not value:
            return value

        if value.isdigit():
            return int(value)

        if value.count(".") and not value.replace(".", "").count("@"):
            return float(value)

        return value


if __name__ == "__main__":
    Console().cmdloop()
