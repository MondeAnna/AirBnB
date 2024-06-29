#!/usr/bin/python3
"""Test suite for inheritor of BaseModel"""
from unittest.mock import MagicMock, patch
from importlib import import_module
import unittest


models = import_module("models")


class TestAll(unittest.TestCase):
    """Collective and specified testing of the `all` method"""

    def setUp(self):
        self.amenity = models.Amenity()
        self.user = models.User()

    @patch("builtins.print")
    def test_all_not_called_when_storage_empty(self, mock_print):
        """Ensure user no printout if storage is empty"""

        models.storage.all = MagicMock(return_value={})
        self.user.all()

        models.storage.all.assert_called_once()
        mock_print.assert_not_called()

    @patch("builtins.print")
    def test_all_not_called_when_instances_not_in_storage(self, mock_print):
        """Ensure user no printout if storage is has no instances"""

        models.storage.all = MagicMock(
            return_value={
                "City.c9eb42a8-bbf1-466e-9720-c3bd3bec417b": {
                    "__class__": "City",
                    "created_at": "2024-06-24T20:16:48.425363",
                    "id": "c9eb42a8-bbf1-466e-9720-c3bd3bec417b",
                    "name": "",
                    "state_id": "",
                    "updated_at": "2024-06-24T20:16:48.425363",
                },
                "Amenity.c38faac4-94c7-4705-93d7-50677d21f922": {
                    "__class__": "Amenity",
                    "created_at": "2024-06-24T20:26:23.358548",
                    "id": "c38faac4-94c7-4705-93d7-50677d21f922",
                    "name": "",
                    "updated_at": "2024-06-24T20:26:23.358548",
                },
            }
        )

        self.user.all()

        models.storage.all.assert_called_once()
        mock_print.assert_not_called()

    @patch("builtins.print")
    def test_all_when_instances_in_storage(self, mock_print):
        """Ensure user is informed when model present"""

        models.storage.all = MagicMock(
            return_value={self.amenity.super_id: self.amenity.to_dict()}
        )

        self.amenity.all()

        models.storage.all.assert_called_once()
        mock_print.assert_called_once_with(self.amenity.super_id)


class TestCount(unittest.TestCase):
    """Collective and specified testing of the `count` method"""

    def setUp(self):
        self.city = models.City()
        self.user = models.User()

    @patch("builtins.print")
    def test_count_prints_none_when_storage_empty(self, mock_print):
        """Ensure printout is zero storage is empty"""

        models.storage.all = MagicMock(return_value={})
        self.user.count()

        models.storage.all.assert_called_once()
        mock_print.assert_called_once_with("User count: 0")

    @patch("builtins.print")
    def test_count_prints_none_when_instances_not_in_storage(self, mock_print):
        """Ensure user no printout if storage is has no instances"""

        models.storage.all = MagicMock(
            return_value={
                "City.c9eb42a8-bbf1-466e-9720-c3bd3bec417b": {
                    "__class__": "City",
                    "created_at": "2024-06-24T20:16:48.425363",
                    "id": "c9eb42a8-bbf1-466e-9720-c3bd3bec417b",
                    "name": "",
                    "state_id": "",
                    "updated_at": "2024-06-24T20:16:48.425363",
                },
                "Amenity.c38faac4-94c7-4705-93d7-50677d21f922": {
                    "__class__": "Amenity",
                    "created_at": "2024-06-24T20:26:23.358548",
                    "id": "c38faac4-94c7-4705-93d7-50677d21f922",
                    "name": "",
                    "updated_at": "2024-06-24T20:26:23.358548",
                },
            }
        )

        self.user.count()

        models.storage.all.assert_called_once()
        mock_print.assert_called_once_with("User count: 0")

    @patch("builtins.print")
    def test_count_when_instances_in_storage(self, mock_print):
        """Ensure user is informed when model present"""

        models.storage.all = MagicMock(
            return_value={self.city.super_id: self.city.to_dict()}
        )

        self.city.count()

        models.storage.all.assert_called_once()
        mock_print.assert_called_once_with("City count: 1")


class TestShow(unittest.TestCase):
    """Collective and specified testing of the `show` method"""

    def setUp(self):
        self.review = models.Review()
        self.state = models.State()

    @patch("builtins.print")
    def test_show_informs_not_found_when_storage_empty(self, mock_print):
        """Ensure user informed no instance is found if storage empty"""

        models.storage.all = MagicMock(return_value={})
        self.state.show("jibberish identification")

        models.storage.all.assert_called_once()
        mock_print.assert_called_once_with("** no instance found **")

    @patch("builtins.print")
    def test_show_informs_not_found_when_instance_not_in_storage(
        self, mock_print
    ):
        """Ensure user informed no instance is found if not in storage"""

        models.storage.all = MagicMock(
            return_value={
                "City.c9eb42a8-bbf1-466e-9720-c3bd3bec417b": {
                    "__class__": "City",
                    "created_at": "2024-06-24T20:16:48.425363",
                    "id": "c9eb42a8-bbf1-466e-9720-c3bd3bec417b",
                    "name": "",
                    "state_id": "",
                    "updated_at": "2024-06-24T20:16:48.425363",
                },
                "Amenity.c38faac4-94c7-4705-93d7-50677d21f922": {
                    "__class__": "Amenity",
                    "created_at": "2024-06-24T20:26:23.358548",
                    "id": "c38faac4-94c7-4705-93d7-50677d21f922",
                    "name": "",
                    "updated_at": "2024-06-24T20:26:23.358548",
                },
            }
        )

        """the uuid goes with the storage's City kwargs"""
        self.state.show("c9eb42a8-bbf1-466e-9720-c3bd3bec417b")

        models.storage.all.assert_called_once()
        mock_print.assert_called_once_with("** no instance found **")

    @patch("builtins.print")
    def test_show_when_instances_in_storage(self, mock_print):
        """Ensure user is informed when model present"""

        models.storage.all = MagicMock(
            return_value={self.review.super_id: self.review.to_dict()}
        )

        self.review.show(self.review.id)

        print_call_arg = mock_print.call_args[0][0]

        self.assertEqual(print_call_arg, self.review)

        models.storage.all.assert_called_once()
        mock_print.assert_called_once()


class TestUser(unittest.TestCase):
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


class TestAmenity(unittest.TestCase):
    """Collective testing of base model attributes"""

    def setUp(self):
        """Provide a factory for test instances"""

        self.amenity = models.Amenity()

    def test_initialisation_has_empty_attr(self):
        """Ensure that all attributes init to empty strings"""

        self.assertEqual(self.amenity.name, "")

    def test_inheritance(self):
        """Assert is subclass of BaseModel"""

        self.assertTrue(issubclass(models.Amenity, models.BaseModel))

    def test_init_with_kwargs(self):
        kwargs = {
            "__class__": "Amenity",
            "id": "0aff3461-4768-4d00-9a2e-0d58ce3e4a58",
            "created_at": "2024-06-24T19:31:15.007629",
            "updated_at": "2024-06-24T19:31:15.007629",
            "name": "Garage Gym",
        }

        amenity = models.Amenity(**kwargs)
        self.assertEqual(amenity.to_dict(), kwargs)


class TestCity(unittest.TestCase):
    """Collective testing of base model attributes"""

    def setUp(self):
        """Provide a factory for test instances"""

        self.city = models.City()

    def test_initialisation_has_empty_attr(self):
        """Ensure that all attributes init to empty strings"""

        self.assertEqual(self.city.name, "")
        self.assertEqual(self.city.state_id, "")

    def test_inheritance(self):
        """Assert is subclass of BaseModel"""

        self.assertTrue(issubclass(models.City, models.BaseModel))

    def test_init_with_kwargs(self):
        kwargs = {
            "__class__": "City",
            "id": "0aff3461-4768-4d00-9a2e-0d58ce3e4a58",
            "created_at": "2024-06-24T19:31:15.007629",
            "updated_at": "2024-06-24T19:31:15.007629",
            "state_id": "57ad4815-937a-46d7-a900-b760d4aff195",
            "name": "Mthatha",
        }

        city = models.City(**kwargs)
        self.assertEqual(city.to_dict(), kwargs)


class TestPlace(unittest.TestCase):
    """Collective testing of base model attributes"""

    def setUp(self):
        """Provide a factory for test instances"""

        self.place = models.Place()

    def test_initialisation_has_empty_attr(self):
        """Ensure that all attributes init to empty strings"""

        self.assertEqual(self.place.city_id, "")
        self.assertEqual(self.place.user_id, "")
        self.assertEqual(self.place.name, "")
        self.assertEqual(self.place.description, "")

        self.assertEqual(self.place.number_rooms, 0)
        self.assertEqual(self.place.number_bathrooms, 0)
        self.assertEqual(self.place.max_guest, 0)
        self.assertEqual(self.place.price_by_night, 0)

        self.assertEqual(self.place.latitude, 0.0)
        self.assertEqual(self.place.longitude, 0.0)

        self.assertEqual(self.place.amenity_ids, [])

    def test_inheritance(self):
        """Assert is subclass of BaseModel"""

        self.assertTrue(issubclass(models.Place, models.BaseModel))

    def test_init_with_kwargs(self):
        kwargs = {
            "__class__": "Place",
            "id": "0aff3461-4768-4d00-9a2e-0d58ce3e4a58",
            "created_at": "2024-06-24T19:31:15.007629",
            "updated_at": "2024-06-24T19:31:15.007629",
            "city_id": "0aff3461-4768-4d00-9a2e-0d58ce3e4a58",
            "user_id": "2937317e-040e-4ed5-881c-6e6c5874212d",
            "name": "Den of Dreams",
            "description": "dreamy",
            "number_rooms": 3,
            "number_bathrooms": 1,
            "max_guest": 1,
            "price_by_night": 890,
            "latitude": 29.8587,
            "longitude": 31.0218,
            "amenity_ids": [
                "57ad4815-937a-46d7-a900-b760d4aff195",
                "c9eb42a8-bbf1-466e-9720-c3bd3bec417b",
            ],
        }

        place = models.Place(**kwargs)
        self.assertEqual(place.to_dict(), kwargs)


class TestReview(unittest.TestCase):
    """Collective testing of base model attributes"""

    def setUp(self):
        """Provide a factory for test instances"""

        self.review = models.Review()

    def test_initialisation_has_empty_attr(self):
        """Ensure that all attributes init to empty strings"""

        self.assertEqual(self.review.place_id, "")
        self.assertEqual(self.review.user_id, "")
        self.assertEqual(self.review.text, "")

    def test_inheritance(self):
        """Assert is subclass of BaseModel"""

        self.assertTrue(issubclass(models.Review, models.BaseModel))

    def test_init_with_kwargs(self):
        kwargs = {
            "__class__": "Review",
            "id": "0aff3461-4768-4d00-9a2e-0d58ce3e4a58",
            "created_at": "2024-06-24T19:31:15.007629",
            "updated_at": "2024-06-24T19:31:15.007629",
            "place_id": "c9eb42a8-bbf1-466e-9720-c3bd3bec417b",
            "user_id": "57ad4815-937a-46d7-a900-b760d4aff195",
            "text": "best ice-cream ever",
        }

        review = models.Review(**kwargs)
        self.assertEqual(review.to_dict(), kwargs)


class TestState(unittest.TestCase):
    """Collective testing of base model attributes"""

    def setUp(self):
        """Provide a factory for test instances"""

        self.state = models.State()

    def test_initialisation_has_empty_attr(self):
        """Ensure that all attributes init to empty strings"""

        self.assertEqual(self.state.name, "")

    def test_inheritance(self):
        """Assert is subclass of BaseModel"""

        self.assertTrue(issubclass(models.State, models.BaseModel))

    def test_init_with_kwargs(self):
        kwargs = {
            "__class__": "State",
            "id": "0aff3461-4768-4d00-9a2e-0d58ce3e4a58",
            "created_at": "2024-06-24T19:31:15.007629",
            "updated_at": "2024-06-24T19:31:15.007629",
            "name": "Eastern Cape",
        }

        state = models.State(**kwargs)
        self.assertEqual(state.to_dict(), kwargs)


if __name__ == "__main__":
    unittest.main()
