"""Utilities functions for the application."""
import redis
import json

import config_layer

POS_DIFF_KEY = 'POS'
NEG_DIFF_KEY = 'NEG'


def merge_subscriptions_and_descriptions(subscriptions, descriptions):
    """Merge a user subscriptions list and the application-wide descriptions.

    From a single user's subscriptions and the application-wide descriptions,
    returns a list dicts. For each entry in the application-wide descriptions, a
    dict is returned in the returned list. If a corresponding entry exists in
    subscriptions, a resultant dict is returned with a True 'subscribed'
    attribute, else the 'subscribed' attribute is false.

    @param subscriptions: A list of subscriptions list names
    @type subscriptions: iterable over list names
    @param descriptions: A dict of subscriptions of the form: {
        'listname': {'description': 'listdescription'},
        ...
    }
    @type subscriptions: iterable over list name and description.
    @return: A dict of dicts, each dict is of the form: {
        'listname': {
            'description': 'listdescription',
            'subscribed': True/False
        }
    }
    @rtype: iterable over dicts
    """
    results = {}
    if not descriptions:
        return results

    for name, item in descriptions.iteritems():
        if name == '_id':
            continue

        results[name] = {
            'description': item.get('description', ''),
            'subscribed': name in subscriptions
        }
    return results


def get_diff(old_subscriptions, new_subscriptions):
    """Compares two iterables of subscriptions to calculate the difference.

    Calculates the positive and negative difference between two iterables of
    subscriptions.

    @param old_subscriptions: The subscriptions that will be considered older.
        May be a list of subscribed subscription names or a dict that has
        subscription names as keys and a dict with an attribute
        'subscribed' = True/False
    @type old_subscriptions: list of str or dict of dicts
    @param new_subscriptions: The subscriptions that will be considered newer.
        May be a list of subscribed subscription names or a dict that has
        subscription names as keys and a dict with an attribute
        'subscribed' = True/False
    @type new_subscriptions: list of str or dict of dicts
    @return: A dict with the two attributes POS_DIFF_KEY and NEG_DIFF_KEY.
        POS_DIFF_KEY refers to a list of subscription names that are in
        new_subscriptions but not in old_subscriptions.
        NEG_DIFF_KEY refers to a list of subscription names that are in
        old_subscriptions but not in new_subscriptions.
    @rtype: iterable over list
    """
    old = set(coerce_to_subscription_name_list(old_subscriptions))
    new = set(coerce_to_subscription_name_list(new_subscriptions))

    intersection = new & old
    pos_dif = new - intersection
    neg_dif = old - intersection

    diff = {
        POS_DIFF_KEY: pos_dif,
        NEG_DIFF_KEY: neg_dif
    }
    return diff


def coerce_to_subscription_name_list(subscriptions):
    """Converts subscriptions into a list of subscription names if needed.

    @param subscriptions: The subscriptions to be coerced.
        May be a list of subscription names or a dict that has
        subscription names as keys and a dict with an attribute
        'subscribed' = True/False
    @type subscriptions: list of str or dict of dicts
    @return: The subscriptions in the form of a list of subscription names
    @type subscriptions: list of str
    """
    if isinstance(subscriptions, dict):
        iteritems = subscriptions.iteritems()
        return [x for x, subscr in iteritems if subscr['subscribed'] == True]

    if isinstance(subscriptions, list):
        return subscriptions

    raise TypeError('Invalid subscriptions type')


class AppConfigKeeper:
    """Singleton for providing global access to the app's configs."""

    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance == None:
            raise ValueError('AppConfigKeeper not initalized')
        return cls.__instance

    @classmethod
    def create_instance(cls, config):
        if cls.__instance != None:
            return
        cls.__instance = AppConfigKeeper(config)

    def __init__(self, config):
        self.__config = config

    def get_app_config(self):
        return self.__config


def get_app_config():
    """Get the application configs.

    @return: The configs
    @type: flask.Config
    """
    return AppConfigKeeper.get_instance().get_app_config()


class AppRedisKeeper:
    """Singleton for providing global access to the app's Redis connection."""

    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance == None:
            cls.__instance = AppRedisKeeper()
        return cls.__instance

    def __init__(self):
        config_settings = config_layer.get_config()

        host = config_settings['REDIS_HOST']
        port = config_settings['REDIS_PORT']
        db = config_settings['REDIS_DB']
        password = config_settings['REDIS_PASSWORD']
        expiration = config_settings['REDIS_EXPIRATION']

        self.redis_conn = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password
        )


def get_redis_connection():
    """Get the Redis cache connection.

    @return: The Redis connection
    @rtype: redis.Redis
    """
    return AppRedisKeeper.get_instance().redis_conn


def args_to_str(*args):
    return ','.join(map(str, args))


def get_redis_key(func, *args):
    func_str = func
    if not isinstance(func, basestring):
        func_str = func.__name__

    return func_str + args_to_str(args).replace('.', '_dot_')


def redis_cached(cache_miss_func):
    """Decorator that caches a function + parameters to a Redis instance.
    """
    config_settings = config_layer.get_config()
    expiration = config_settings['REDIS_EXPIRATION']

    def inner(*args, **kwargs):
        key = get_redis_key(cache_miss_func, args)

        redis_conn = get_redis_connection()
        prior = redis_conn.get(key)

        if not prior:
            ret_val = cache_miss_func(*args, **kwargs)
            redis_conn.setex(key, json.dumps(ret_val), expiration)
            print 'set ' + key
        else:
            ret_val = json.loads(prior)

        return ret_val


    def inner_guarded(*args, **kwargs):
        try:
            # Try to connect to the redis cache and get cached value
            return inner(*args, **kwargs)
        except Exception as e:
            # If failed to connect to redis cache
            print 'cache fail -', e
            return cache_miss_func(*args, **kwargs)

    return inner_guarded


def get_template_folders(is_module):
    template_folder_temp='../templates'
    static_folder_temp='../static'

    if not is_module:
        template_folder_temp='templates',
        static_folder_temp='static'

    return {
        'template_folder': template_folder_temp,
        'static_folder': static_folder_temp
    }

