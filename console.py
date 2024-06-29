#!/usr/bin/python3
"""CLI Backend Console"""
from collections import OrderedDict
import cmd


from models.base_model import BaseModel
from models import storage


class Console(cmd.Cmd):
    """CLI Backend Console"""

    __MODELS = {"BaseModel": BaseModel}
    prompt = "(anna) "

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

        if model_name and model_name not in self.__MODELS:
            return print("** model doesn't exist **")

        if not model_name:
            list_of_kwargs = list(storage.all().values())
        else:
            list_of_kwargs = [
                kwargs for kwargs in storage.all().values()
                if kwargs.get("__class__") == model_name
            ]

        for kwargs in list_of_kwargs:
            model = self.__MODELS.get(kwargs.get("__class__"))
            print(model(**kwargs).super_id)

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

        Missing Model Name
        ------------------
            (anna) create
            ** model name missing **

        Non-Existant Model
        ------------------
            (anna) create DoesNotExist
            ** model doesn't exist **
        """

        if not self.__is_valid_model__(model_name):
            return

        Model = self.__MODELS.get(model_name)
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

        if not self.__is_valid_model__(parsed["model_name"]):
            return

        if not self.__is_valid_id__(parsed["instance_id"]):
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

        if not self.__is_valid_model__(parsed["model_name"]):
            return

        if not self.__is_valid_id__(parsed["instance_id"]):
            return

        key = f"{parsed.get('model_name')}.{parsed.get('instance_id')}"
        kwargs = storage.all().get(key)
        print(BaseModel(**kwargs))

    def do_update(self, line):
        """
        Updates an instance based on the model name and id
        by adding or updating attribute, which is then sent
        to storage. One attribute can be updated at a time,
        whereby the attribute value is cast into one of
        three type, float, int or str.

        Of note is that `id`, `created_at` and `updated_at`
        cannot be updated.

        Usage
        -----
            update <model name> <id> <attribute name> "<attribute value>"

        Expected
        --------
            (anna) update BaseModel 1234-1234-1234 email "aibnb@mail.com"

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
            (anna) update BaseModel
            ** instance id missing **

        Non-Existant Instance ID
        ------------------------
            (anna) update BaseModel 123-456-789
            ** no instance found **

        Missing Attribute Name
        ----------------------
            (anna) update BaseModel 123-456-789
            ** attribute name missing **

        Non-Existant Attribute Value
        ----------------------------
            (anna) update BaseModel 123-456-789 first_name
            ** value missing **
        """

        parsed = self.__parse_line__(line)

        if not self.__is_valid_model__(parsed["model_name"]):
            return

        if not self.__is_valid_id__(parsed["instance_id"]):
            return

        if not parsed["attribute"]:
            return print("** attribute name missing **")

        if not parsed["value"]:
            return print("** value missing **")

        key = f"{parsed.get('model_name')}.{parsed.get('instance_id')}"
        kwargs = storage.all().get(key)

        if parsed.get("attribute"):
            attr = parsed.get("attribute")
            kwargs[attr] = parsed.get("value")

        Model = self.__MODELS.get(parsed["model_name"])
        model = Model(**kwargs)
        storage.save()

    def emptyline(self):
        """Skips to new prompt should input be empty"""

        pass

    def __is_valid_id__(self, instance_id):
        """Validates instance id as being existant"""

        keys = storage.all().keys()
        elements = [element for key in keys for element in key.split(".")]

        if not instance_id:
            print("** instance id missing **")
            return False

        if instance_id not in elements:
            print("** no instance found **")
            return False

        return True

    def __is_valid_model__(self, model_name):
        """Validates model name as being existant"""

        if not model_name:
            print("** model name missing **")
            return False

        if model_name not in self.__MODELS:
            print("** model doesn't exist **")
            return False

        return True

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

        parsed = OrderedDict({
            "model_name": None,
            "instance_id": None,
            "attribute": None,
            "value": None,
        })

        split = line.split()

        for key, value in zip(parsed, split):
            parsed[key] = value

        parsed["value"] = self.__type_value(parsed["value"])

        return parsed

    @staticmethod
    def __type_value(value):
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

        for instance in [float, int, str]:
            if isinstance(value, instance):
                return instance(value)


if __name__ == "__main__":
    Console().cmdloop()
