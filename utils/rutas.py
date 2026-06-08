import os
from core.config_manager import cargar_config

def obtener_ruta_archivos(tipo='general'):

    config = cargar_config()
    base = config.get('ruta_archivos')
    ruta = os.path.join(base, tipo)

    # Crear carpeta si no existe
    if not os.path.exists(ruta):
        os.makedirs(ruta)
    return ruta

def obtener_ruta_updates():

    config = cargar_config()
    ruta = config.get('ruta_updates')

    if not ruta:
        raise Exception('No existe ruta_updates')
    os.makedirs(ruta, exist_ok=True)
    return ruta