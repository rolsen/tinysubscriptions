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

    configuration = services.util.get_app_config()

    return flask.render_template(
        'mailing_chrome.html',
        base_url=configuration['BASE_URL'],
        app_title=APP_TITLE,
        email=email,
        lists=subscriptions,
        base_static_folder=configuration['BASE_STATIC_URL']
    )


def update_lists(email):
    """Updates the user list subscriptions."""
    subscrip_service = services.subscriptions_service

    old_subscriptions = subscrip_service.get_user_subscriptions(email)
    new_subscriptions = json.loads(flask.request.form.get('subscriptions'))

    diff = services.util.get_diff(old_subscriptions, new_subscriptions)

    if len(diff[POS_DIFF_KEY]) > 0:
        response = subscrip_service.subscribe(email, diff[POS_DIFF_KEY])
        if response.status_code != 200:
            return response.text, response.status_code

    if len(diff[NEG_DIFF_KEY]) > 0:
        response = subscrip_service.unsubscribe(email, diff[NEG_DIFF_KEY])
        if response.status_code != 200:
            return response.text, response.status_code

    return 'success', 200
