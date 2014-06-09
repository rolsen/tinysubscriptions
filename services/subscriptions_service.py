"""Underlying service to manage the email subscriptions.

@author: Rory Olsen (rolsen, Gleap LLC 2014)
"""
import sendgrid

import util


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
    def subscribe(cls, email, new_subscriptions):
        print "FakeSendGrid.subscribe"

    @classmethod
    def unsubscribe(cls, email, cancel_subscriptions):
        print "FakeSendGrid.unsubscribe"


def get_user_subscriptions(email):
    """Get all lists the specified user email is subscribed to.

    Get all lists the specified user email is subscribed to from the real
    SendGrid service or the fake SendGrid service if the FAKE_SENDGRID config is
    True.

    @param email: The user email for which to return list subscriptions.
    @type email: str
    @return: Dict of the form: {
        'listname 0':'description 0',
        'listname 1':'description 1',
        ...
    }
    @rtype: iterable over lists
    """
    if util.get_app_config()['FAKE_SENDGRID']:
        return FakeSendGrid.get_subscriptions(email)

    print "get_user_subscriptions stub"
    # https://api.sendgrid.com/api/unsubscribes.get.json
    # ?api_user=your_sendgrid_username
    # &api_key=your_sendgrid_password
    # &email={{ email }}
    return [
        'subscriptions_service.get_user_subscriptions stub'
    ]


def subscribe(email, new_subscriptions):
    """Subscribe a user for a given set of lists.

    Subscribe a user for a given set of lists using the real SendGrid service or
    the fake SendGrid service if the FAKE_SENDGRID config is True.

    @param email: email address corresponding to a user
    @type email: str
    @parm new_subscriptions: the subscriptions to subscribe the user
        from.
    @type new_subscriptions: iterable over str
    """
    if util.get_app_config()['FAKE_SENDGRID']:
        return FakeSendGrid.subscribe(email, new_subscriptions)

    print "subscribe stub", new_subscriptions


def unsubscribe(email, cancel_subscriptions):
    """Unsubscribe a user for a given set of lists.

    Unsubscribe a user for a given set of lists using the real SendGrid service
    or the fake SendGrid service if the FAKE_SENDGRID config is True.

    @param email: email address corresponding to a user
    @type email: str
    @parm cancel_subscriptions: the subscriptions to unsubscribe the user
        from.
    @type cancel_subscriptions: iterable over str
    """
    if util.get_app_config()['FAKE_SENDGRID']:
        return FakeSendGrid.unsubscribe(email, cancel_subscriptions)

    print "unsubscribe stub", cancel_subscriptions
