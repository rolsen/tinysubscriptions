"""Utilities functions for the application."""

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
        'listname': 'listdescription'
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
    for name, description in descriptions.iteritems():
        results[name] = {
            'description': description,
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
