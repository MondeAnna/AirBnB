#!/usr/bin/python3
"""Tests for the products console"""
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from importlib import import_module
import unittest
import uuid


import console

models = import_module("models")


class TestConsole(unittest.TestCase):
    """Tests for the products console"""

    def setUp(self):
        """Test instance factory"""

        self.model = models.BaseModel()

        self.user = models.User()
        self.user.save = MagicMock()

        models.storage.new = MagicMock()
        models.storage.save = MagicMock()
        models.storage.all = MagicMock(
            return_value={self.user.super_id: self.user.to_dict()}
        )

    def test_quit(self):
        """Ensures that the user can exit the console"""

        self.assertTrue(console.Console().onecmd("EOF"))
        self.assertTrue(console.Console().onecmd("quit"))


class TestDefault(TestConsole):
    """Tests cases for the `default` method"""

    @patch("builtins.print")
    def test_default_with_valid_model(self, mock_print):
        """Ensures that repl command is executed when valid"""

        console.Console().default("User.all()")
        mock_print.assert_called_once_with(self.user.super_id)

    @patch("builtins.print")
    def test_default_with_unknown_value(self, mock_print):
        """Ensures that repl command is executed when valid"""

        console.Console().default("Jibberish")
        mock_print.assert_called_once_with("** unknown syntax: Jibberish **")


class TestAll(TestConsole):
    """Tests cases for the `do_all` method"""

    @patch("builtins.print")
    def test_all_when_no_models_present(self, mock_print):
        """Ensures that no model is show if none present"""

        models.storage.all = MagicMock(return_value={})
        console.Console().do_all("")
        mock_print.assert_not_called()

    @patch("builtins.print")
    def test_when_only_all_is_inputted(self, mock_print):
        """
        Ensures that all models are shown

        In order to emulate cmd.Cmd actively taking `no input`,
        an empty string has to be provided in the test case
        """

        console.Console().do_all("")
        mock_print.assert_called_once()

    @patch("builtins.print")
    def test_all_valid_model_provided(self, mock_print):
        """Ensures that valid model shows available models"""

        console.Console().do_all("User")
        mock_print.assert_called_once()

    @patch("builtins.print")
    def test_all_with_invalid_model(self, mock_print):
        """Ensures that user is informed if invalid model is provided"""

        console.Console().do_all("invalid")
        mock_print.assert_called_once_with("** model doesn't exist **")


class TestCreate(TestConsole):
    """Tests cases for the `do_create` method"""

    @patch("builtins.print")
    def test_create_with_valid_model(self, mock_print):
        """Ensures that a new model can be created"""

        console.Console().do_create("User")

        model_id = mock_print.call_args[0][0]
        new_uuid = uuid.UUID(model_id, version=4)

        self.assertTrue(isinstance(new_uuid, uuid.UUID))
        mock_print.assert_called_once()

    @patch("builtins.print")
    def test_create_without_providing_a_model(self, mock_print):
        """
        Ensures that user is informed of need to provide a model

        In order to emulate cmd.Cmd actively taking `no input`,
        an empty string has to be provided in the test case
        """

        console.Console().do_create("")
        mock_print.assert_called_once_with("** model name missing **")

    @patch("builtins.print")
    def test_create_with_an_invalid_model(self, mock_print):
        """Ensures that user is informed in model is invalid"""

        console.Console().do_create("invalid")
        mock_print.assert_called_once_with("** model doesn't exist **")


class TestDestroy(TestConsole):
    """Tests cases for the `do_destroy` method"""

    def test_destroy_with_valid_input(self):
        """Ensures that existing model can be destroyed"""

        console.Console().do_destroy(f"User {self.user.id}")

        """a secondary call is made when parsing id"""
        self.assertEqual(models.storage.all.call_count, 2)
        models.storage.save.assert_called_once()

    @patch("builtins.print")
    def test_destroy_without_providing_input(self, mock_print):
        """
        Ensures that user is informed of need for both a
        model and an id

        In order to emulate cmd.Cmd actively taking `no input`,
        an empty string has to be provided in the test case
        """

        console.Console().do_destroy("")
        mock_print.assert_called_once_with("** model name missing **")

        models.storage.all.assert_not_called()
        models.storage.save.assert_not_called()

    @patch("builtins.print")
    def test_destroy_using_invalid_model(self, mock_print):
        """Ensures that user is informed in model is invalid"""

        console.Console().do_destroy("Ice-Cream-Chicken-Popcorn-Coffee")
        mock_print.assert_called_once_with("** model doesn't exist **")

        models.storage.all.assert_not_called()
        models.storage.save.assert_not_called()

    @patch("builtins.print")
    def test_destroy_without_providing_an_id(self, mock_print):
        """Ensures that user is informed of the need of in id"""

        console.Console().do_destroy("User")
        mock_print.assert_called_once_with("** instance id missing **")

        """a call is made when parsing id"""
        models.storage.all.assert_called_once()
        models.storage.save.assert_not_called()

    @patch("builtins.print")
    def test_destroy_when_no_match_is_found(self, mock_print):
        """Ensures that user is informed if no match is found"""

        console.Console().do_destroy("User 1234-1234-1234-1234")
        mock_print.assert_called_once_with("** no instance found **")

        """a call is made when parsing id"""
        models.storage.all.assert_called_once()
        models.storage.save.assert_not_called()


class TestShow(TestConsole):
    """Tests cases for the `do_show` method"""

    @patch("builtins.print")
    def test_show_with_valid_input(self, mock_print):
        """
        Ensures that existing model can be shown

        ID not tested as User looks to create a different id
        even when kwargs are provided during init
        """

        console.Console().do_show(f"User {self.user.id}")
        call_arg = mock_print.call_args[0][0]

        call_created = call_arg.to_dict().get("created_at")
        model_created = self.user.to_dict().get("created_at")

        call_updated = call_arg.to_dict().get("updated_at")
        model_updated = self.user.to_dict().get("updated_at")

        self.assertEqual(call_created, model_created)
        self.assertEqual(call_updated, model_updated)

        self.assertEqual(type(call_arg), type(self.user))

        """a secondary call is made when parsing id"""
        self.assertEqual(models.storage.all.call_count, 2)
        mock_print.assert_called_once()

    @patch("builtins.print")
    def test_show_without_providing_input(self, mock_print):
        """
        Ensures that user is informed of need for both a
        model and an id

        In order to emulate cmd.Cmd actively taking `no input`,
        an empty string has to be provided in the test case
        """

        console.Console().do_show("")
        mock_print.assert_called_once_with("** model name missing **")
        models.storage.all.assert_not_called()

    @patch("builtins.print")
    def test_show_using_invalid_model(self, mock_print):
        """Ensures that user is informed in model is invalid"""

        console.Console().do_show("Ice-Cream-Chicken-Popcorn-Coffee")
        mock_print.assert_called_once_with("** model doesn't exist **")
        models.storage.all.assert_not_called()

    @patch("builtins.print")
    def test_show_without_providing_an_id(self, mock_print):
        """Ensures that user is informed of the need of in id"""

        console.Console().do_show("User")
        mock_print.assert_called_once_with("** instance id missing **")

        """a call is made when parsing id"""
        self.assertEqual(models.storage.all.call_count, 1)

    @patch("builtins.print")
    def test_show_with_when_match_is_found(self, mock_print):
        """Ensures that user is informed if no match is found"""

        console.Console().do_show("User 1234-1234-1234-1234")
        mock_print.assert_called_once_with("** no instance found **")

        """a call is made when parsing id"""
        self.assertEqual(models.storage.all.call_count, 1)


class TestUpdate(TestConsole):
    """Tests cases for the `do_update` method"""

    def test_update_when_all_parameters_present(self):
        """
        Ensure that update operates as expected

        NOTE: Unable to prove that the model in memory has been updated
        """

        cmd = f"User {self.user.id} name BestNameEver"
        console.Console().do_update(cmd)

        self.user.save.assert_called_once()

    def test_update_email(self):
        """Ensure that updating email does not cause an error"""

        cmd = f"User {self.user.id} email user@email.com"
        console.Console().do_update(cmd)

        self.user.save.assert_called_once()

    @patch("builtins.print")
    def test_update_without_providing_input(self, mock_print):
        """
        Ensures that user is informed of need for both a
        model and an id

        In order to emulate cmd.Cmd actively taking `no input`,
        an empty string has to be provided in the test case
        """

        console.Console().do_update("")
        mock_print.assert_called_once_with("** model name missing **")
        models.storage.all.assert_not_called()

    @patch("builtins.print")
    def test_update_using_invalid_model(self, mock_print):
        """Ensures that user is informed in model is invalid"""

        console.Console().do_update("Ice-Cream-Chicken-Popcorn-Coffee")
        mock_print.assert_called_once_with("** model doesn't exist **")
        models.storage.all.assert_not_called()

    @patch("builtins.print")
    def test_update_without_providing_an_id(self, mock_print):
        """Ensures that user is informed of the need of in id"""

        console.Console().do_update("User")
        mock_print.assert_called_once_with("** instance id missing **")

        """a call is made when parsing id"""
        self.assertEqual(models.storage.all.call_count, 1)

    @patch("builtins.print")
    def test_update_with_when_match_is_found(self, mock_print):
        """Ensures that user is informed if no match is found"""

        console.Console().do_update("User 1234-1234-1234-1234")
        mock_print.assert_called_once_with("** no instance found **")

        """a call is made when parsing id"""
        self.assertEqual(models.storage.all.call_count, 1)

    @patch("builtins.print")
    def test_update_with_when_attribute_name_is_missing(self, mock_print):
        """Ensures that user is informed if no attribute provided"""

        console.Console().do_update(f"User {self.user.id}")
        mock_print.assert_called_once_with("** attribute name missing **")

        """a call is made when parsing id"""
        self.assertEqual(models.storage.all.call_count, 1)

    @patch("builtins.print")
    def test_update_with_when_immutable_attribut_given(self, mock_print):
        """Ensures that user is informed if immutable attribute provided"""

        console.Console().do_update(f"User {self.user.id} id")
        mock_print.assert_called_with("** immutable attribute **")

        console.Console().do_update(f"User {self.user.id} created_at")
        mock_print.assert_called_with("** immutable attribute **")

        console.Console().do_update(f"User {self.user.id} updated_at")
        mock_print.assert_called_with("** immutable attribute **")

        """a call is made when parsing id"""
        self.assertEqual(models.storage.all.call_count, 3)

    @patch("builtins.print")
    def test_update_with_when_value_missing(self, mock_print):
        """Ensures that user is informed if no value provided"""

        console.Console().do_update(f"User {self.user.id} name")
        mock_print.assert_called_once_with("** value missing **")

        """a call is made when parsing id"""
        self.assertEqual(models.storage.all.call_count, 1)


if __name__ == "__main__":
    unittest.main()
