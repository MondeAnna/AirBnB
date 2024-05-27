#!/usr/bin/python3
"""
Collective testing of attributes
related to base model
"""


from unittest.mock import MagicMock
from unittest.mock import patch
from datetime import datetime
from unittest import TestCase
from unittest import main
import uuid


from models.base_model import BaseModel
from models import storage


class TestBaseModel(TestCase):
    """
    Collective testing of attributes
    related to base model
    """

    def setUp(self):
        """Test instance factory"""

        self.model_00 = BaseModel()
        self.model_01 = BaseModel()
        storage.save = MagicMock()

    @staticmethod
    def expect_exception(attribute, model):
        return f"property '{attribute}' of '{model}' object has no setter"


class TestIdentification(TestBaseModel):
    """
    Collective and specified testing
    of the `id` model attribute
    """

    def test_id_is_str(self):
        """Instance ID is str type"""

        id_ = self.model_00.id
        self.assertIsInstance(id_, str)

    def test_id_is_unique(self):
        """Instance ID's are unique to each instance"""

        id_00 = self.model_00.id
        id_01 = self.model_01.id
        self.assertNotEqual(id_00, id_01)

    def test_id_is_immutable(self):
        """Instance ID cannot be unchangeable after instantiation"""

        with self.assertRaises(AttributeError) as error:
            self.model_01.id = "new id"

        expect = self.expect_exception("id", "BaseModel")
        exception = str(error.exception)

        self.assertEqual(exception, expect)

    def test_super_id(self):
        """Instance ID suffixed to model type"""

        super_id = self.model_00.super_id
        id_ = self.model_00.id

        self.assertEqual(super_id, f"BaseModel.{id_}")
        self.assertIsInstance(super_id, str)


class TestCreatedAt(TestBaseModel):
    """
    Collective and specified testing of
    the `created_at` model attribute
    """

    def test_created_at_is_datetime(self):
        """Instance attribute is datetime object"""

        created_at = self.model_01.created_at
        self.assertIsInstance(created_at, datetime)

    def test_created_at_is_unique_to_instance(self):
        """Instance attribute is unique to each instance"""

        created_at_00 = self.model_00.created_at
        created_at_01 = self.model_01.created_at
        self.assertNotEqual(created_at_00, created_at_01)

    def test_created_at_is_immutable(self):
        """Instance attribute unchangeable after instantiation"""

        with self.assertRaises(AttributeError) as error:
            self.model_00.created_at = datetime.now()

        expect = self.expect_exception("created_at", "BaseModel")
        exception = str(error.exception)

        self.assertEqual(exception, expect)


class TestUpdatedAt(TestBaseModel):
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

        updated_at = self.model_00.updated_at
        self.assertIsInstance(updated_at, datetime)

    def test_updated_at_is_publicly_immutable(self):
        """Instance attribute publicly immutable"""

        with self.assertRaises(AttributeError) as error:
            self.model_00.updated_at = datetime.now()

        expect = self.expect_exception("updated_at", "BaseModel")
        exception = str(error.exception)

        self.assertEqual(exception, expect)

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

        expect_created_at = datetime(2017, 9, 28, 21, 3, 54, 52298)
        expect_updated_at = datetime(2017, 9, 30, 13, 33, 33, 52302)

        self.assertEqual(model.created_at, expect_created_at)
        self.assertEqual(model.updated_at, expect_updated_at)

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


class TestSave(TestBaseModel):
    """Collective testing of `save` method"""

    def test_calling_save_alters_updated_at_attr(self):
        """Instance `update_at` alterd when method called"""

        creation_datetime = self.model_00.created_at
        original_datetime = self.model_00.updated_at

        self.model_00.save()

        updated_datetime = self.model_00.updated_at

        storage.save.assert_called_once()

        self.assertNotEqual(creation_datetime, updated_datetime)
        self.assertNotEqual(original_datetime, updated_datetime)


class TestInitMocking(TestCase):
    """Setup objects used across multiple mocked tests"""

    @patch("models.base_model.uuid", wraps=uuid)
    @patch("models.base_model.datetime", wraps=datetime)
    def setUp(self, mock_dt, mock_uuid):
        mock_uuid.uuid4.return_value = "unique id"

        self.init_time = datetime.now()
        mock_dt.now.return_value = self.init_time
        self.init_time_str = self.init_time.isoformat()

        self.model = BaseModel()


class TestToDict(TestInitMocking):
    """Collective testing of `to_dict` method"""

    def test_to_dict_attr_value_pair_provision(self):
        """Evaluate instance attributes-value pairing"""

        expect = {
            "__class__": "BaseModel",
            "created_at": self.init_time_str,
            "id": "unique id",
            "updated_at": self.init_time_str,
        }

        self.assertEqual(self.model.to_dict(), expect)

    def test_to_dict_after_adding_new_attribute(self):
        """
        Evaluate instance attributes-value pairing when
        the addition of a new attribute is made
        """

        self.model.new_attr = "new attribute"

        expect = {
            "__class__": "BaseModel",
            "created_at": self.init_time_str,
            "id": "unique id",
            "new_attr": "new attribute",
            "updated_at": self.init_time_str,
        }

        dict_ = self.model.to_dict()

        self.assertNotEqual(dict_.get("updated_at"), expect.get("updated_at"))
        self.assertEqual(dict_.get("created_at"), expect.get("created_at"))

        self.assertEqual(dict_.get("__class__"), expect.get("__class__"))
        self.assertEqual(dict_.get("new_attr"), expect.get("new_attr"))
        self.assertEqual(dict_.get("id"), expect.get("id"))


class TestDunderStr(TestInitMocking):
    """Collective testing of `__str__` property"""

    def test_str_property(self):
        """Instance str representation standardised layout"""

        dict_ = {
            "created_at": self.init_time,
            "id": "unique id",
            "updated_at": self.init_time,
        }

        expect = f"[BaseModel] (unique id) {dict_}"
        actual = str(self.model)

        self.assertEqual(actual, expect)


if __name__ == "__main__":
    main()
