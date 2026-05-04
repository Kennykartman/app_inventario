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
