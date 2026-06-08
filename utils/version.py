import json
import os
import sys
import logging
from utils.rutas import (obtener_ruta_updates)

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))

VERSION_LOCAL = os.path.join(BASE_DIR, 'config', 'version.json')



def obtener_version_local():

    with open(
        VERSION_LOCAL,
        'r',
    ) as f:
        data = json.load(f)
    return data['version']

def obtener_version_remota():

    ruta = os.path.join(
        obtener_ruta_updates(),
        'version.json'
    )
    with open(
        ruta,
        'r',
    ) as f:
        data = json.load(f)
    return data['version']

def obtener_changelog():
    ruta = os.path.join(
        obtener_ruta_updates(),
        'changelog.txt'
        )

    try:
        with open(
            ruta,
            'r',
            encoding='utf-8'
        ) as f:
            return f.read()
    except FileNotFoundError:
        logging.warning(
            'No existe changelog.txt'
        )

        return 'sin descripcion'
