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
        self.storage._FileStorage__objects = {}

        self.file_path = "file.json"

        self.model_00 = MagicMock(id="model_00")
        self.model_01 = MagicMock(id="model_01")

        self.model_00.super_id = "BaseModel.model_00"
        self.model_01.super_id = "BaseModel.model_01"

        self.model_00.to_dict.return_value = {
            "super_id": self.model_00.super_id,
            "id": "model_00",
            "__class__": "BaseModel",
        }

        self.model_01.to_dict.return_value = {
            "super_id": self.model_01.super_id,
            "id": "model_01",
            "__class__": "BaseModel",
        }


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

    def test_new_when_single_model_is_provided(self):
        """Ensures the provided instance is tracked"""

        self.storage.new(self.model_00)

        models = self.storage.all()
        num_models = len(models)

        self.assertTrue(self.model_00.to_dict() in models.values())
        self.assertEqual(num_models, 1)

    def test_new_tracking_via_class_name_and_id_combo(self):
        """
        Ensures tracking is a combo of the class name
        and instance id
        """

        self.storage.new(self.model_01)

        models = self.storage.all()
        num_models = len(models)

        self.assertTrue("BaseModel.model_01" in models.keys())
        self.assertEqual(num_models, 1)

    def test_new_multiple_additions_made(self):
        """Ensure operable with multiple additions"""

        self.storage.new(self.model_00)
        self.storage.new(self.model_01)

        models = self.storage.all()
        num_models = len(models)

        self.assertTrue(self.model_01.to_dict() in models.values())
        self.assertTrue("BaseModel.model_00" in models.keys())
        self.assertEqual(num_models, 2)


class TestSave(TestFileStorage):
    """Ensure serialisation to JSON file"""

    @patch("json.dump")
    @patch("builtins.open")
    @patch("pathlib.Path.touch")
    @patch("pathlib.Path.is_file", return_value=False)
    def test_save_with_no_file_on_system(
        self, mock_is_file, mock_touch, mock_open, mock_dump
    ):
        """Ensure creates a new file if none present"""

        self.storage.save()

        mock_is_file.assert_called_once_with()
        mock_touch.assert_called_once()

        mock_open.assert_called_once_with(self.file_path, "w")
        mock_dump.assert_called_once_with({}, mock_open().__enter__())

    @patch("json.dump")
    @patch("builtins.open")
    @patch("pathlib.Path.is_file", return_value=True)
    def test_save_with_cached_models(self, mock_if_file, mock_open, mock_dump):
        """Ensures writes to file when cached models present"""

        cache = {self.model_00.super_id: self.model_00.to_dict()}

        self.storage.new(self.model_00)
        self.storage.save()

        mock_open.assert_called_once_with(self.file_path, "w")
        mock_dump.assert_called_once_with(cache, mock_open().__enter__())


class TestReload(TestFileStorage):
    """Assert deserialisation to json file"""

    mock_load_side_effect = {
        "BaseModel.2ef7469a-9b12-4174-97a3-89744af13dbd": {
            "__class__": "BaseModel",
            "created_at": "2024-03-09T10:33:34.745168",
            "id": "2ef7469a-9b12-4174-97a3-89744af13dbd",
            "updated_at": "2024-03-09T10:33:34.745168",
        }
    }

    @patch("json.dump")
    @patch("builtins.open")
    @patch("pathlib.Path.is_file", return_value=False)
    def test_reload_with_no_file_present(
        self, mock_is_file, mock_open, mock_dump
    ):
        """Ensure reload does crash the system if no file present"""

        try:
            self.storage.reload()
        except Exception as exception:
            message = exception.args[0]
            self.fail(message)

        self.assertEqual(self.storage.all(), {})

    @patch("json.load", return_value={})
    @patch("builtins.open")
    @patch("pathlib.Path.stat")
    @patch("pathlib.Path.is_file", return_value=True)
    def test_reload_resets_cache_when_file_is_empty(
        self, mock_is_file, mock_stat, mock_open, mock_load
    ):
        """Ensure reloading empty file empties cache"""

        mock_stat.return_value.st_size = 0

        self.storage.new(self.model_01)
        pre_call = self.storage.all()

        self.storage.reload()

        post_call = self.storage.all()

        mock_is_file.assert_called_once()
        mock_stat.assert_called_once()

        mock_open.assert_not_called()
        mock_load.assert_not_called()

        self.assertNotEqual(pre_call, post_call)
        self.assertEqual(post_call, {})

    @patch("json.load")
    @patch("builtins.open")
    @patch("pathlib.Path.stat")
    @patch("pathlib.Path.is_file", return_value=True)
    def test_reload_when_non_empty_file_exits(
        self, mock_is_file, mock_stat, mock_open, mock_load
    ):
        """Ensure reloading with a non-empty refreshes cache"""

        mock_stat.return_value.st_size = 10
        mock_load.return_value = self.mock_load_side_effect

        pre_call = self.storage.all()
        self.storage.reload()
        post_call = self.storage.all()

        mock_is_file.assert_called_once()
        mock_stat.assert_called_once()

        mock_open.assert_called_once_with(self.file_path, "r")
        mock_load.assert_called_once()

        self.assertNotEqual(pre_call, post_call)


if __name__ == "__main__":
    main()
