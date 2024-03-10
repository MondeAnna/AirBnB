#!/usr/bin/python3


"""
Test suite for the user module
"""


from importlib import import_module
from unittest import TestCase
from unittest import main


models = import_module("models")


class TestUser(TestCase):

    """Collective testing of base model attributes"""

    def setUp(self):
        """Provide a factory for test instances"""

        self.user = models.User()

    def test_initialisation_has_empty_attr(self):
        """Ensure that all attributes init to empty strings"""

        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")
        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")

    def test_inheritance(self):
        """Assert is subclass of BaseModel"""

        self.assertTrue(issubclass(models.User, models.BaseModel))

    def test_init_with_kwargs(self):
        """Ensure that new instances can be created with saved data"""

        kwargs = {
            "__class__": "User",
            "id": "0aff3461-4768-4d00-9a2e-0d58ce3e4a58",
            "created_at": "2024-06-24T19:31:15.007629",
            "updated_at": "2024-06-24T19:31:15.007629",
            "first_name": "first",
            "last_name": "last",
            "email": "first.last@email.com",
            "password": "best3ma!L",
        }

        user = models.User(**kwargs)
        self.assertEqual(user.to_dict(), kwargs)


if __name__ == "__main__":
    main()
