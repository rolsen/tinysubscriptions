"""Controller for admins to control which listings may be subscribed to.

@author: Rory Olsen (rolsen, Gleap LLC 2014)
@license: GNU GPLv3
"""
import functools

import flask
import json

# Optimally, it would be nice to have "is_module" controlled by the configs, but
# they may not be available when this module is imported.
is_module = True

try:
    from tinysubscriptions import services
    from tinysubscriptions.services import config_layer
except:
    import services
    from services import config_layer
    is_module = False


blueprint = flask.Blueprint(
    'descriptions',
    __name__,
    **services.util.get_template_folders(is_module)
)


def require_admin(target_func):
    @functools.wraps(target_func)
    def inner_func(*args, **kwargs):
        if services.config_layer.cur_user_is_admin():
            return target_func(*args, **kwargs)
        else:
            flask.abort(403)
    return inner_func


@blueprint.route('/admin_lists', methods=['GET'])
@require_admin
def get_lists():
    """Get the subscription lists information."""
    descriptions = services.descriptions_service.get_descriptions()
    subscriptions = services.subscriptions_service.get_lists()

    if not descriptions:
        descriptions = {}

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
    temp_vals = services.config_layer.get_common_template_vals()
    parent_template = config_layer.get_config().get('BASE_TEMPLATE', 'base.html')

    return flask.render_template(
        'admin_chrome.html',
        base_url=configuration['BASE_URL'],
        app_title='Subscription Admin Center',
        base_static_url=configuration['BASE_STATIC_URL'],
        lists=lists,
        base_static_folder=configuration['BASE_STATIC_URL'],
        parent_template=parent_template,
        **temp_vals
    )


@blueprint.route('/admin_lists', methods=['POST'])
@require_admin
def update_lists():
    """Update the subscription lists information.

    Update which subscription lists are available to non-admin users as well as
    update the subscription lists' names and descriptions.
    """
    new_descriptions = json.loads(flask.request.form.get('descriptions'))
    services.descriptions_service.update_descriptions(new_descriptions)
    return 'success', 200
