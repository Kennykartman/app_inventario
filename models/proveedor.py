from models.base_model import BaseModel

class Proveedor(BaseModel):

    @staticmethod
    def crear(nombre, direccion, correo, pagina, entidad, clasificacion):

        conexion = Proveedor()

        sql = '''
        INSERT INTO  proveedores
            (nombre, direccion, correo, pagina, entidad, clasificacion)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''

        conexion. ejecutar_query(
            sql,
            (nombre, direccion, correo, pagina, entidad, clasificacion)
        )

    @staticmethod
    def listar():

        conexion = Proveedor()

        sql = '''
        SELECT id_proveedor, nombre, direccion, correo, pagina, entidad, clasificacion
        FROM proveedores
              '''

        return conexion.ejecutar_query(sql, fetch=True)