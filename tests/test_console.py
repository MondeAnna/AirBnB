#!/usr/bin/python3
"""Tests for the products console"""
from unittest.mock import MagicMock, patch
import unittest
import uuid


from models.base_model import BaseModel
from models import storage
import console


class TestConsole(unittest.TestCase):
    """Tests for the products console"""

    def setUp(self):
        """Test instance factory"""

        self.model = BaseModel()
        storage.save = MagicMock()
        storage.all = MagicMock(
            return_value={self.model.super_id: self.model}
        )

    def test_quit(self):
        """Ensures that the user can exit the console"""

        self.assertTrue(console.Console().onecmd("EOF"))
        self.assertTrue(console.Console().onecmd("quit"))


class TestCreate(TestConsole):
    """Tests cases for the `do_create` method"""

    @patch("builtins.print")
    def test_create_with_valid_model(self, mock_print):
        """Ensures that a new model can be created"""

        console.Console().do_create("BaseModel")

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

        console.Console().do_destroy(f"BaseModel {self.model.id}")

        """a secondary call is made when parsing id"""
        self.assertEqual(storage.all.call_count, 2)
        storage.save.assert_called_once()

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

        storage.all.assert_not_called()
        storage.save.assert_not_called()

    @patch("builtins.print")
    def test_destroy_using_invalid_model(self, mock_print):
        """Ensures that user is informed in model is invalid"""

        console.Console().do_destroy("Ice-Cream-Chicken-Popcorn-Coffee")
        mock_print.assert_called_once_with("** model doesn't exist **")

        storage.all.assert_not_called()
        storage.save.assert_not_called()

    @patch("builtins.print")
    def test_destroy_without_providing_an_id(self, mock_print):
        """Ensures that user is informed of the need of in id"""

        console.Console().do_destroy("BaseModel")
        mock_print.assert_called_once_with("** instance id missing **")

        """a call is made when parsing id"""
        storage.all.assert_called_once()
        storage.save.assert_not_called()

    @patch("builtins.print")
    def test_destroy_when_no_match_is_found(self, mock_print):
        """Ensures that user is informed if no match is found"""

        console.Console().do_destroy("BaseModel 1234-1234-1234-1234")
        mock_print.assert_called_once_with("** no instance found **")

        """a call is made when parsing id"""
        storage.all.assert_called_once()
        storage.save.assert_not_called()


class TestShow(TestConsole):
    """Tests cases for the `do_show` method"""

    @patch("builtins.print")
    def test_show_with_valid_input(self, mock_print):
        """Ensures that existing model can be shown"""

        console.Console().do_show(f"BaseModel {self.model.id}")
        mock_print.assert_called_once_with(self.model)

        """a secondary call is made when parsing id"""
        self.assertEqual(storage.all.call_count, 2)

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
        storage.all.assert_not_called()

    @patch("builtins.print")
    def test_show_using_invalid_model(self, mock_print):
        """Ensures that user is informed in model is invalid"""

        console.Console().do_show("Ice-Cream-Chicken-Popcorn-Coffee")
        mock_print.assert_called_once_with("** model doesn't exist **")
        storage.all.assert_not_called()

    @patch("builtins.print")
    def test_show_without_providing_an_id(self, mock_print):
        """Ensures that user is informed of the need of in id"""

        console.Console().do_show("BaseModel")
        mock_print.assert_called_once_with("** instance id missing **")

        """a call is made when parsing id"""
        self.assertEqual(storage.all.call_count, 1)

    @patch("builtins.print")
    def test_show_with_when_match_is_found(self, mock_print):
        """Ensures that user is informed if no match is found"""

        console.Console().do_show("BaseModel 1234-1234-1234-1234")
        mock_print.assert_called_once_with("** no instance found **")

        """a call is made when parsing id"""
        self.assertEqual(storage.all.call_count, 1)


if __name__ == "__main__":
    unittest.main()
