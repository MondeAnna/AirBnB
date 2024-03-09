#!/usr/bin/python3
"""CLI Backend Console"""
import cmd


from models.base_model import BaseModel


class Console(cmd.Cmd):
    """CLI Backend Console"""

    __MODELS = ["BaseModel"]
    prompt = "(anna) "

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

        model = BaseModel()
        model.save()
        print(model.id)

    def do_EOF(self, line):
        """Exits the programme when user enters `ctrl+d`"""

        print()
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""

        return True

    def emptyline(self):
        """Skips to new prompt should input be empty"""

        pass

    def __is_valid_model__(self, model_name):
        """Validates model name as being existant"""

        if not model_name:
            print("** model name missing **")
            return False

        if model_name not in self.__MODELS:
            print("** model doesn't exist **")
            return False

        return True


if __name__ == "__main__":
    Console().cmdloop()
