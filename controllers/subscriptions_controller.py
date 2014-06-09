"""Controller for users to control which listings they are subscribed to.

@author: Rory Olsen (rolsen, Gleap LLC 2014)
@license: GNU GPLv3
"""
import flask
import json

import services

POS_DIFF_KEY = services.util.POS_DIFF_KEY
NEG_DIFF_KEY = services.util.NEG_DIFF_KEY

APP_TITLE = 'Subscription Center'

blueprint = flask.Blueprint(
    'subscriptions',
    __name__,
    template_folder='templates'
)


@blueprint.route('/manage_lists', methods=['GET', 'POST'])
def manage_lists():
    email = flask.request.args.get('email', None)
    if not email:
        return 'No email provied', 404

    if flask.request.method == 'GET':
        return get_lists(email)
    elif flask.request.method == 'POST':
        return update_lists(email)


def get_lists(email):
    """Render controls to change what lists a user is subscribed to."""
    subscriptions = services.subscriptions_service.get_user_subscriptions(email)
    descriptions = services.descriptions_service.get_descriptions()

    subscriptions = services.util.merge_subscriptions_and_descriptions(
        subscriptions,
        descriptions
    )

    return flask.render_template(
        'mailing_chrome.html',
        base_url=services.util.get_app_config()['BASE_URL'],
        app_title=APP_TITLE,
        email=email,
        lists=subscriptions
    )


def update_lists(email):
    """Updates the user list subscriptions."""
    old_subscriptions = services.subscriptions_service.get_user_subscriptions(
        email
    )
    new_subscriptions = json.loads(flask.request.form.get('subscriptions'))

    diff = services.util.get_diff(old_subscriptions, new_subscriptions)
    services.subscriptions_service.subscribe(email, diff[POS_DIFF_KEY])
    services.subscriptions_service.unsubscribe(email, diff[NEG_DIFF_KEY])

    return 'success', 200
