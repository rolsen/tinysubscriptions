"""Server for the SendGrid-based subscription manager.

Serves an interface for end-users for the managing the lists that they are
subscribed to, as well as an interface for admin-users to manage which lists are
available for end-user subscription.

@author: Rory Olsen (rolsen, Gleap LLC 2014)
@license: GNU GPLv3
"""
import flask
from flask.ext.pymongo import PyMongo
import json

import config_cache

import controllers
import services

def attach_blueprints(target_app):
    target_app.register_blueprint(
        controllers.descriptions_controller.blueprint,
        url_prefix='/mailing'
    )
    target_app.register_blueprint(
        controllers.subscriptions_controller.blueprint,
        url_prefix='/mailing'
    )


def get_app():
    return config_cache.get_config()['app']


def initialize_standalone():
    # Initialize
    app = flask.Flask(__name__)
    config_cache.get_config()['app'] = app

    # Load configuration settings
    app.config.update(services.config_layer.get_config())

    # Create singleton for access
    services.util.AppConfigKeeper.create_instance(app.config)

    attach_blueprints(app)


if __name__ == '__main__':
    initialize_standalone()

    app = get_app()
    app.config['DEBUG'] = True

    app.run()
