from models.base_model import BaseModel


class FallaModelo(BaseModel):

    def __init__(self, id_modelo=None, descripcion=None, solucion=None, codigo_falla='N/A'):
        self.id_modelo = id_modelo
        self.descripcion = descripcion
        self.solucion = solucion
        self.codigo_falla = (codigo_falla or 'N/A').strip()

    def guardar(self):

        sql = '''
        INSERT INTO fallas_modelo (id_modelo, codigo_falla, descripcion, solucion)
        VALUES (%s, %s, %s, %s)
        '''
        datos = (self.id_modelo,
                 self.codigo_falla,
                 self.descripcion,
                 self.solucion
                 )

        self.ejecutar_query(sql, datos)

    @staticmethod
    def listar_por_modelo(id_modelo):

        conexion = FallaModelo()

        sql = '''
        SELECT codigo_falla, descripcion, solucion
        FROM fallas_modelo
        WHERE id_modelo = %s
        AND activo = True
        '''

        return conexion.ejecutar_query(sql, (id_modelo,), fetch=True)