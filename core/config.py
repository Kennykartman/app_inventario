import psycopg2
from dotenv import load_dotenv
from core.config_manager import cargar_config

load_dotenv()

def conectar():

    config = cargar_config()
    if config.get('modo') == 'servidor':
        host = 'localhost'
    else:
        host = config['host']
    try:
        return psycopg2.connect(
            host=config['host'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            port=config['port']
        )
    except Exception as e:
        print('ERROR DE CONEXION', e)
        return None

def es_servidor():
    config = cargar_config()
    return config.get('modo') == 'servidor'