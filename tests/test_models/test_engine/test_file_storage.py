#!/usr/bin/python3
"""
Test suite regarding the manipulation of data in relation
to file storage and thereby the file system
"""


from unittest.mock import MagicMock
from unittest.mock import patch
from unittest import TestCase
from unittest import main


from models import FileStorage


class TestFileStorage(TestCase):
    """Setup objects used across multiple tests"""

    def setUp(self):
        """Test instance factory"""

        self.storage = FileStorage()
        self.mock_model_00 = MagicMock(id="mock_model_00")
        self.mock_model_01 = MagicMock(id="mock_model_01")

        self.mock_model_00.super_id = "BaseModel.mock_model_00"
        self.mock_model_01.super_id = "BaseModel.mock_model_01"

        self.mock_model_00.to_dict.return_value = {
            "super_id": self.mock_model_00.super_id,
            "id": "mock_model_00",
            "__class__": "BaseModel",
        }

        self.mock_model_01.to_dict.return_value = {
            "super_id": self.mock_model_01.super_id,
            "id": "mock_model_01",
            "__class__": "BaseModel",
        }

    def flush_storage(self):
        """Destroy models presently in storage"""

        self.storage._FileStorage__objects = {}


class TestAll(TestFileStorage):
    """
    Collective and specified testing of the
    retrieval of models from file storage
    """

    def test_all_with_empty_storage(self):
        """Ensure that a new instance has no saved models"""

        self.assertEqual(self.storage.all(), {})


class TestNew(TestFileStorage):
    """
    Collective and specified testing ensuring that new
    instances are cached for serialisation
    """

    def test_new_when_single_object_is_provided(self):
        """Ensures the provided instance is tracked"""

        self.flush_storage()
        self.storage.new(self.mock_model_00)

        models = self.storage.all()
        num_models = len(models)

        self.assertTrue(self.mock_model_00.to_dict() in models.values())
        self.assertEqual(num_models, 1)

    def test_new_tracking_via_class_name_and_id_combo(self):
        """
        Ensures tracking is a combo of the class name
        and instance id
        """

        self.flush_storage()
        self.storage.new(self.mock_model_01)

        models = self.storage.all()
        num_models = len(models)

        self.assertTrue("BaseModel.mock_model_01" in models.keys())
        self.assertEqual(num_models, 1)

    def test_new_multiple_additions_made(self):
        """Ensure operable with multiple additions"""

        self.storage.new(self.mock_model_00)
        self.storage.new(self.mock_model_01)

        models = self.storage.all()
        num_models = len(models)

        self.assertTrue(self.mock_model_01.to_dict() in models.values())
        self.assertTrue("BaseModel.mock_model_00" in models.keys())
        self.assertEqual(num_models, 2)


if __name__ == "__main__":
    main()
