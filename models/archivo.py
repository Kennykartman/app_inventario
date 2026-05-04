import os

from models.base_model import BaseModel

class Archivo(BaseModel):

    @staticmethod
    def guardar(tipo, id_ref, id_equipo, nombre, ruta):

        conexion = Archivo()
        nombre = os.path.basename(ruta)

        sql = '''
        INSERT INTO archivos (tipo, id_ref, id_equipo, nombre, ruta)
            VALUES (%s, %s, %s, %s, %s)
        '''

        conexion.ejecutar_query(sql, [tipo, id_ref, id_equipo, nombre, ruta])

    @staticmethod
    def listar_por_equipo(id_equipo):

        conexion = Archivo()

        sql = '''
        SELECT nombre, tipo, fecha, ruta
        FROM archivos
            where id_equipo = %s
            ORDER BY fecha DESC
        '''
        return conexion.ejecutar_query(sql, [id_equipo], fetch=True)

    @staticmethod
    def obtener_archivo(id_equipo):

        conexion = Archivo()

        sql = '''
        SELECT archivo_asignacion a
        JOIN asignaciones s ON a.id_asignacion = s.id_asignacion
        WHERE s.id_equipo = %s
        '''
        return conexion.ejecutar_query(sql, [id_equipo], fetch=True)
