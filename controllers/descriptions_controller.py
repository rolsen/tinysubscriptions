"""Controller for admins to control which listings may be subscribed to.

@author: Rory Olsen (rolsen, Gleap LLC 2014)
@license: GNU GPLv3
"""
import flask

import services

blueprint = flask.Blueprint(
    'descriptions',
    __name__,
    template_folder='templates'
)

@blueprint.route('/admin_lists')
def admin_lists():
    return flask.render_template(
        'admin_chrome.html',
        base_url=services.util.get_app_config()['BASE_URL'],
        app_title='Subscription Admin Center'
    )
