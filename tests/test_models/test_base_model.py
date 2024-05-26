#!/usr/bin/python3
"""
Collective testing of attributes
related to base model
"""


from datetime import datetime
from unittest import TestCase
from unittest import main


from models import BaseModel


class TestBaseModel(TestCase):
    """
    Collective testing of attributes
    related to base model
    """

    def setUp(self):
        """Test instance factory"""

        self.model_00 = BaseModel()
        self.model_01 = BaseModel()


class TestBaseModelId(TestBaseModel):
    """
    Collective and specified testing
    of the `id` model attribute
    """

    def test_id_is_str(self):
        """Instance ID is str type"""

        is_str = isinstance(self.model_00.id, str)
        self.assertTrue(is_str)

    def test_id_is_unique(self):
        """Instance ID's are unique to each instance"""

        id_00 = self.model_00.id
        id_01 = self.model_01.id
        self.assertNotEqual(id_00, id_01)

    def test_id_is_immutable(self):
        """Instance ID cannot be unchangeable after instantiation"""

        with self.assertRaises(AttributeError) as error:
            self.model_01.id = "new id"

        expected = "property 'id' of 'BaseModel' object has no setter"
        exception = str(error.exception)

        self.assertEqual(exception, expected)


class TestBaseModelCreatedAt(TestBaseModel):
    """
    Collective and specified testing of
    the `created_at` model attribute
    """

    def test_created_at_is_datetime(self):
        """Instance attribute is datetime object"""

        is_datetime = isinstance(self.model_01.created_at, datetime)
        self.assertTrue(is_datetime)

    def test_created_at_is_unique_to_instance(self):
        """Instance attribute is unique to each instance"""

        created_at_00 = self.model_00.created_at
        created_at_01 = self.model_01.created_at
        self.assertNotEqual(created_at_00, created_at_01)

    def test_created_at_is_immutable(self):
        """Instance attribute unchangeable after instantiation"""

        with self.assertRaises(AttributeError) as error:
            self.model_00.created_at = datetime.now()

        expected = "property 'created_at' of 'BaseModel' object has no setter"
        exception = str(error.exception)

        self.assertEqual(exception, expected)


if __name__ == "__main__":
    main()
