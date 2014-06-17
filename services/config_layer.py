import json

with open('flask_config.json', 'r') as f:
    CONFIG_VALUES = json.loads(f.read())


def inject_config(config_values):
    CONFIG_VALUES = config_values


def get_config():
    return CONFIG_VALUES.get('tinysubscriptions', CONFIG_VALUES)
