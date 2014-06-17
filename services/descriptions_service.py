"""Underlying service to configure which lists may be subscribed to.

@author: Rory Olsen (rolsen, Gleap LLC 2014)
"""
from flask.ext.pymongo import PyMongo

import subscriptions_service
import util


def get_descriptions():
    """Get the list descriptions for the application.

    @return: Dict of the form: {
        'listname 0': {'description': 'description text 0 ...'},
        'listname 1': {'description': 'description text 1 ...'},
        ...
    }
    @rtype: iterable over str
    """
    return get_db().subscriptions.find_one()


def update_descriptions(new_descriptions):
    """Upserts the list descriptions for the application.

    @param new_descriptions: The new list descriptions to set, of the form: {
        'listname 0': {'description': 'description text 0 ...'},
        'listname 1': {'description': 'description text 1 ...'},
        ...
    }
    @type new_descriptions: iterable over list descriptions.
    """
    old_record = get_descriptions()
    if old_record:
        the_id = old_record.get('_id', None)
    else:
        the_id = None

    if the_id:
        new_descriptions['_id'] = the_id
    descriptions = dict(
        map(
            lambda (k, v): (k.replace('.', '_dot_'), v),
            new_descriptions.items()
        )
    )
    get_db().subscriptions.save(descriptions)

    util.get_redis_connection().flushall()

    # get_user_subscriptions updates the cache
    subscriptions_service.get_user_subscriptions('test@example.com')


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
            'List Name 0': {'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin pharetra porttitor nisi, in accumsan elit vulputate non. Suspendisse consequat ac enim sit amet placerat. Quisque eleifend nunc metus, eu egestas ante aliquet quis. Morbi magna elit, viverra in pulvinar et, feugiat quis velit. Nam volutpat massa blandit lorem ornare ornare. Etiam adipiscing mi eu lectus mollis, ullamcorper vulputate magna mattis. Praesent sapien lectus, aliquet quis porttitor scelerisque, aliquam non nisi. Nunc sapien libero, tincidunt lobortis sapien quis, tincidunt lobortis lectus. Duis a convallis magna.'},
            'List Name 1': {'description': 'Pellentesque bibendum sem id accumsan consectetur. Pellentesque tincidunt rutrum lorem. Nam congue consequat turpis et aliquet. Suspendisse consequat, lacus non eleifend posuere, massa leo tempor eros, auctor tempus lacus lectus ut lectus. Phasellus lorem urna, faucibus et enim at, lacinia placerat nisl. Suspendisse ut purus eu dolor dignissim mattis. In metus diam, porta quis aliquet sed, sodales quis dui.'},
            'List Name 2': {'description': 'Aenean nec risus nunc. In non massa ut lectus viverra dignissim. Etiam ullamcorper metus a nibh posuere consectetur. Proin porttitor elementum purus, vel volutpat neque blandit a. Ut faucibus blandit varius. Aenean id volutpat leo. Nullam vestibulum tincidunt leo, a porta arcu elementum eget. Morbi eleifend urna at nisi tempus sodales. Integer iaculis lectus eget neque dignissim, id bibendum diam dapibus.'}
        }

    def find_one(self):
        return self.__contents

    def save(self, doc):
        self.__contents = doc


class FakeMongoDB:
    """Test object to imitate a Mongo db. Persists until server restart."""

    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance == None:
            cls.__instance = FakeMongoDB()
        return cls.__instance

    def __init__(self):
        self.subscriptions = FakeCollection()


def get_db():
    """Get the local application database or test database.

    @return: The database, or the test database if the FAKE_MONGO config is True
    @type: flask_pymongo.wrappers.Database
    """
    if util.get_app_config()['FAKE_MONGO']:
        return FakeMongoDB.get_instance()

    return AppMongoKeeper.get_instance().get_mongo().db
