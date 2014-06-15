import json

with open('flask_config.json', 'r') as f:
    CONFIG_VALUS = json.loads(f.read())

def get_config():
    return CONFIG_VALUS
