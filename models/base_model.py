from core.config import conectar

class BaseModel:

    def ejecutar_query(self, sql, datos=None, fetch=False):

        conexion = conectar()

        if not conexion:
            raise Exception('No se puede conectar al servidor')
        cursor = conexion.cursor()

        cursor.execute(sql, datos)

        resultado = None

        if fetch:
            resultado = cursor.fetchall()

        conexion.commit()

        cursor.close()
        conexion.close()

        return resultado