"""Controller for admins to control which listings may be subscribed to.

@author: Rory Olsen (rolsen, Gleap LLC 2014)
@license: GNU GPLv3
"""
import flask
import json

import services

blueprint = flask.Blueprint(
    'descriptions',
    __name__,
    template_folder='templates'
)

@blueprint.route('/admin_lists', methods=['GET'])
def get_lists():
    """Get the subscription lists information."""
    descriptions = services.descriptions_service.get_descriptions()
    subscriptions = services.subscriptions_service.get_lists()

    lists = []
    for listname in subscriptions:
        description_item = descriptions.get(listname, None)
        description = ''
        if description_item:
            description = description_item.get('description', None)

        lists.append({
            'name': listname,
            'description': description,
            'is_managed': description_item != None
        })

    configuration = services.util.get_app_config()

    return flask.render_template(
        'admin_chrome.html',
        base_url=configuration['BASE_URL'],
        app_title='Subscription Admin Center',
        base_static_url=configuration['BASE_STATIC_URL'],
        lists=lists
    )


@blueprint.route('/admin_lists', methods=['POST'])
def update_lists():
    """Update the subscription lists information.

    Update which subscription lists are available to non-admin users as well as
    update the subscription lists' names and descriptions.
    """
    new_descriptions = json.loads(flask.request.form.get('descriptions'))
    services.descriptions_service.update_descriptions(new_descriptions)
    return 'success', 200
