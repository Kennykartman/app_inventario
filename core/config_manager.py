import json
import os
import sys
import logging

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
                        )
            )

CONFIG_FILE = os.path.join(BASE_DIR, 'config', 'config.json')

def cargar_config():

    if not os.path.exists(CONFIG_FILE):
        logging.warning(
            f'No existe config:\n{CONFIG_FILE}'
        )
        return None

    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def guardar_config(data):
    print("CONFIG FILE:")
    print(CONFIG_FILE)
    os.makedirs(
        os.path.dirname(CONFIG_FILE),
        exist_ok=True
    )

    with open(
        CONFIG_FILE,
        'w'
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )