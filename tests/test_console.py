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


if __name__ == "__main__":
    unittest.main()
