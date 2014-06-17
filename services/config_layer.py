import json

try:
    with open('flask_config.json', 'r') as f:
        CONFIG_VALUES = json.loads(f.read())
except IOError:
    CONFIG_VALUES = {}

GET_COMMON_TEMPLATE_VALS_INNER = {'target': lambda: {}}

CUR_USER_IS_ADMIN_INNER = {'target': lambda: True}


def inject_config(config_values):
    CONFIG_VALUES = config_values


def get_config():
    return CONFIG_VALUES.get('tinysubscriptions', CONFIG_VALUES)


def set_cur_user_is_admin_func(func):
    CUR_USER_IS_ADMIN_INNER['target'] = func


def set_common_template_vals_func(func):
    GET_COMMON_TEMPLATE_VALS_INNER['target'] = func


def cur_user_is_admin():
    return CUR_USER_IS_ADMIN_INNER['target']()


def get_common_template_vals():
    return GET_COMMON_TEMPLATE_VALS_INNER['target']()
