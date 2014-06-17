import json

try:
    with open('flask_config.json', 'r') as f:
        CONFIG_VALUES = json.loads(f.read())
except IOError:
    CONFIG_VALUES = {}


print 'herlksadjflasdjf'
GET_COMMON_TEMPLATE_VALS_INNER = {'target': lambda: {}}


def inject_config(config_values):
    CONFIG_VALUES = config_values


def get_config():
    return CONFIG_VALUES.get('tinysubscriptions', CONFIG_VALUES)


def set_common_template_vals_func(func):
    print 'halkjdsflaksdjf!'
    print func
    GET_COMMON_TEMPLATE_VALS_INNER['target'] = func


def get_common_template_vals():
    print GET_COMMON_TEMPLATE_VALS_INNER
    return GET_COMMON_TEMPLATE_VALS_INNER['target']()
