"""Underlying service to configure which lists may be subscribed to.

@author: Rory Olsen (rolsen, Gleap LLC 2014)
"""
from flask.ext.pymongo import PyMongo

import util


def get_descriptions():
    """Get the list descriptions for the application.

    @return: Dict of the form: {
        'listname 0':'description 0',
        'listname 1':'description 1',
        ...
    }
    @rtype: iterable over str
    """
    return get_db().subscriptions.find_one()


def update_descriptions(new_descriptions):
    """Upserts the list descriptions for the application.

    @param new_descriptions: The new list descriptions to set, of the form: {
        'listname 0': 'description 0',
        'listname 1': 'description 1',
        ...
    }
    @type new_descriptions: iterable over list descriptions.
    """
    return get_db().subscriptions.save()


class AppMongoKeeper:
    """Singleton for providing global access to the app's Mongo database."""

    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance == None:
            raise ValueError('AppMongoKeeper not initalized')
        return cls.__instance

    @classmethod
    def create_instance(cls, mongo):
        if cls.__instance != None:
            return
        cls.__instance = AppMongoKeeper(mongo)

    def __init__(self, mongo):
        self.__mongo = mongo

    def get_mongo(self):
        return self.__mongo


class FakeCollection:
    """Test object to imitate a sub-domain of Mongo functionality."""

    def __init__(self):
        self.__contents = {
            'List Name 0': 'description 0',
            'List Name 1': 'description 1',
            'List Name 2': 'description 2'
        }

    def find_one(self):
        return self.__contents

    def save(self, doc):
        self.__contents = doc


class FakeMongoDB:

    subscriptions = FakeCollection()


def get_db():
    """Get the local application database or test database.

    @return: The database, or the test database if the FAKE_MONGO config is True
    @type: flask_pymongo.wrappers.Database
    """
    if util.get_app_config()['FAKE_MONGO']:
        return FakeMongoDB()

    return AppMongoKeeper.get_instance().get_mongo().db
