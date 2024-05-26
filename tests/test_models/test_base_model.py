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

    @staticmethod
    def expected_exception(attribute, model):
        return f"property '{attribute}' of '{model}' object has no setter"


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

        expected = self.expected_exception("id", "BaseModel")
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

        expected = self.expected_exception("created_at", "BaseModel")
        exception = str(error.exception)

        self.assertEqual(exception, expected)


class TestBaseModelUpdatedAt(TestBaseModel):
    """
    Collective and specified testing of
    the `updated_at` model attribute
    """

    kwargs = {
        "id": "56d43177-cc5f-4d6c-a0c1-e167f8c27337",
        "created_at": "2017-09-28T21:03:54.052298",
        "my_number": 89,
        "updated_at": "2017-09-30T13:33:33.052302",
        "name": "My_First_Model",
    }

    def test_updated_at_is_datetime(self):
        """Instance attribute is datetime object"""

        is_datetime = isinstance(self.model_00.updated_at, datetime)
        self.assertTrue(is_datetime)

    def test_updated_at_is_publicly_immutable(self):
        """Instance attribute publicly immutable"""

        with self.assertRaises(AttributeError) as error:
            self.model_00.updated_at = datetime.now()

        expected = self.expected_exception("updated_at", "BaseModel")
        exception = str(error.exception)

        self.assertEqual(exception, expected)

    def test_updated_at_altered_by_augmenting_object(self):
        """Instance alterations alter `updated_at` value"""

        creation_datetime = self.model_01.created_at
        original_datetime = self.model_01.updated_at

        self.model_01.change = 5

        updated_datetime = self.model_01.updated_at

        self.assertNotEqual(creation_datetime, updated_datetime)
        self.assertNotEqual(original_datetime, updated_datetime)

    def test_update_at_unaltered_when_init_with_kwargs(self):
        """Instance spawned with kwargs does not alter `updated_at`"""

        model = BaseModel(**self.kwargs)

        expected_created_at = datetime(2017, 9, 28, 21, 3, 54, 52298)
        expected_updated_at = datetime(2017, 9, 30, 13, 33, 33, 52302)

        self.assertEqual(model.created_at, expected_created_at)
        self.assertEqual(model.updated_at, expected_updated_at)

        self.assertEqual(model.my_number, self.kwargs.get("my_number"))
        self.assertEqual(model.name, self.kwargs.get("name"))
        self.assertEqual(model.id, self.kwargs.get("id"))

    def test_will_drop(self):
        """Use kwargs spawned by other instance for accuracy"""

        dict_ = self.model_00.to_dict()
        new_model = BaseModel(**dict_)

        self.assertEqual(self.model_00.id, new_model.id)
        self.assertEqual(self.model_00.created_at, new_model.created_at)
        self.assertEqual(self.model_00.updated_at, new_model.updated_at)


class TestBaseModelSaveMethod(TestBaseModel):
    """Collective testing of `save` method"""

    def test_calling_save_alters_updated_at_attr(self):
        """Instance `update_at` alterd when method called"""

        creation_datetime = self.model_00.created_at
        original_datetime = self.model_00.updated_at

        self.model_00.save()

        updated_datetime = self.model_00.updated_at

        self.assertNotEqual(creation_datetime, updated_datetime)
        self.assertNotEqual(original_datetime, updated_datetime)


if __name__ == "__main__":
    main()
