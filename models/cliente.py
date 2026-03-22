from models.base_model import BaseModel

class Cliente(BaseModel):

    def __init__(self, nombre=None, direccion=None, telefono = None, email=None, contrato=None):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.contrato = contrato

    def guardar(self):

        sql = '''
        INSERT INTO clientes (nombre, direccion, telefono, email, no_contrato)
        VALUES (%s, %s, %s, %s, %s)
        '''

        datos = (
            self.nombre,
            self.direccion,
            self.telefono,
            self.email,
            self.contrato
        )

        self.ejecutar_query(sql, datos)

    @staticmethod
    def listar():

        conexion = Cliente()

        sql = '''
        SELECT id_cliente, nombre, direccion, telefono, email, no_contrato
        FROM clientes
        WHERE activo = True
        ORDER BY nombre
        '''

        return conexion.ejecutar_query(sql, fetch=True)
