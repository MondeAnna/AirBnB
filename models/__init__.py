#!/usr/bin/python3
"""Pre-Initial vital system components"""


from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


"""subclasses of BaseModel need be imported after"""


from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


ALL_MODELS = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


storage = FileStorage()
storage.reload()
