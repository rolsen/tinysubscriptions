"""Underlying service to manage the email subscriptions.

@author: Rory Olsen (rolsen, Gleap LLC 2014)
"""
import json

import requests
import sendgrid

import util

SENDGRID_BASE_API_URL = 'https://api.sendgrid.com/api%s.json'

SENDGRID_ACTION_URLS = {
    'GET_LISTS': '/newsletter/lists/get',
    'ADD_USER_IN_LIST': '/newsletter/lists/email/add',
    'GET_USERS_IN_LIST': '/newsletter/lists/email/get',
    'DELETE_USER_IN_LIST': '/newsletter/lists/email/delete'
}

def post_sendgrid(url, data_params=None):
    """Make a sendgrid HTTPS post to a sendgrid url with some optional data.

    @param url: The sendgrid url to post to.
    @type url: str
    @param data_params: Any additional data parameters to send. User credentials
        are not required.
    @type data_params: dict
    @return: The response from sendgrid.
    @rtype: requests.models.Response
    """
    data = {
        'api_user': util.get_app_config()['SENDGRID_API_USERNAME'],
        'api_key': util.get_app_config()['SENDGRID_API_KEY']
    }
    if data_params:
        data.update(data_params)

    sendgrid_url = SENDGRID_BASE_API_URL % url
    response = requests.post(
        sendgrid_url,
        data=data
    )

    if response.status_code != 200:
        print "Sendgrid %d. url: %s, data_params: %s, reason: %s" % (
            response.status_code,
            sendgrid_url,
            str(data_params),
            response.text
        )
    return response


class FakeSendGrid:
    """Test object to imitate a sub-domain of SendGrid functionality."""

    __contents = [
        'List Name 0',
        'List Name 1',
        'List Name 3',
        'Invisible List Name'
    ]

    @classmethod
    def get_subscriptions(cls, email):
        return cls.__contents

    @classmethod
    def get_lists(cls):
        return cls.__contents

    @classmethod
    def subscribe(cls, email, new_subscriptions):
        print "FakeSendGrid.subscribe"

    @classmethod
    def unsubscribe(cls, email, cancel_subscriptions):
        print "FakeSendGrid.unsubscribe"


@util.redis_cached
def get_lists():
    """Get all lists that are available for subscription.

    @return: Array of mailing lists.
    @rtype: iterable over str
    """
    if util.get_app_config()['FAKE_SENDGRID']:
        return FakeSendGrid.get_lists()

    response = post_sendgrid(SENDGRID_ACTION_URLS['GET_LISTS'])
    if response.status_code == 200:
        data = response.json()
        return [x['list'] for x in data]

    else:
        return []


@util.redis_cached
def list_emails_subscribed_to_list(listname):
    """List all emails subscribed to a SengGrid mailing list.

    @param listname: The mailing list name for which to list subscribed emails.
    @type listname: str
    @return: An array of email addresses.
    @rtype: Iterable over str
    """
    response = post_sendgrid(
        SENDGRID_ACTION_URLS['GET_USERS_IN_LIST'],
        {
            'list': listname.replace('_dot_', '.')
        }
    )
    if response.status_code != 200:
        print """list_emails_subscribed_to_list error.
        %d - %s
        Server restart or cache invalidation is needed.""" % (
            response.status_code,
            response.text
        )

    return [x['email'] for x in response.json()]


@util.redis_cached
def get_user_subscriptions(email):
    """Get all lists the specified user email is subscribed to.

    Get all lists the specified user email is subscribed to from the real
    SendGrid service or the fake SendGrid service if the FAKE_SENDGRID config is
    True.

    @param email: The user email for which to return list subscriptions.
    @type email: str
    @return: Array of mailing lists
    @rtype: iterable over str
    """
    if util.get_app_config()['FAKE_SENDGRID']:
        return FakeSendGrid.get_subscriptions(email)

    lists = get_lists()
    subscriptions = []
    for item in lists:
        if email in list_emails_subscribed_to_list(item):
            subscriptions.append(item)

    return subscriptions


def upsert_list(redis, set_operation, func, param, value):
    key = util.get_redis_key(func, (param,))
    prior = redis.get(key)
    if prior:
        prior = json.loads(prior)
        value = getattr(set(prior), set_operation)(set([value]))

    else:
        value = [value]

    redis.set(key, json.dumps(list(value)))


def subscribe(email, new_subscriptions):
    """Subscribe a user for a given set of lists.

    Subscribe a user for a given set of lists using the real SendGrid service or
    the fake SendGrid service if the FAKE_SENDGRID config is True.

    @param email: email address corresponding to a user
    @type email: str
    @parm new_subscriptions: the subscriptions to subscribe the user
        from.
    @type new_subscriptions: iterable over str
    @return: The first failing response from SendGrid, the last successful
        response from SendGrid, or None if new_subscriptions is len() = 0
    @rtype: requests.models.Response
    """
    if util.get_app_config()['FAKE_SENDGRID']:
        return FakeSendGrid.subscribe(email, new_subscriptions)

    data_str = """{
        "email":"%s",
        "name":"%s"
    }""" % (
        email,
        email.split('@')[0] # Get up until the @ and send that as the name
    )
    response = None
    for subscription in new_subscriptions:
        # Subscribe via SendGrid
        response = post_sendgrid(
            SENDGRID_ACTION_URLS['ADD_USER_IN_LIST'],
            {
                'list': subscription.replace('_dot_', '.'),
                'data': data_str
            }
        )
        if response.status_code != 200:
            return response

        # Update the main cache
        redis = util.get_redis_connection()
        upsert_list(redis, 'union', 'list_emails_subscribed_to_list',
            subscription, value=subscription)

        # Upsert a per user cache
        upsert_list(redis, 'union', 'get_user_subscriptions', email,
            value=subscription)

    return response


def unsubscribe(email, cancel_subscriptions):
    """Unsubscribe a user for a given set of lists.

    Unsubscribe a user for a given set of lists using the real SendGrid service
    or the fake SendGrid service if the FAKE_SENDGRID config is True.

    @param email: email address corresponding to a user
    @type email: str
    @parm cancel_subscriptions: the subscriptions to unsubscribe the user
        from.
    @type cancel_subscriptions: iterable over str
    @return: The first failing response from SendGrid, the last successful
        response from SendGrid, or None if cancel_subscriptions is len() = 0
    @rtype: requests.models.Response
    """
    if util.get_app_config()['FAKE_SENDGRID']:
        return FakeSendGrid.unsubscribe(email, cancel_subscriptions)

    response = None
    for subscription in cancel_subscriptions:
        # Unsubscribe via SendGrid
        response = post_sendgrid(
            SENDGRID_ACTION_URLS['DELETE_USER_IN_LIST'],
            {
                'list': subscription.replace('_dot_', '.'),
                'email': email
            }
        )
        if response.status_code != 200:
            return response

        # Update the main cache
        redis = util.get_redis_connection()
        upsert_list(redis, 'difference', 'list_emails_subscribed_to_list',
            subscription, value=subscription)

        # Upsert the per user cache
        upsert_list(redis, 'difference', 'get_user_subscriptions', email,
            value=subscription)

    return response
