from models.base_model import BaseModel
from models.mantenimiento import Mantenimiento


class Modelo(BaseModel):

    def __init__(self,
                 marca_fabricante=None,
                 modelo_fabricante=None,
                 marca_comercial=None,
                 modelo_comercial=None,
                 descripcion=None):

        self.marca_fabricante = marca_fabricante
        self.modelo_fabricante = modelo_fabricante
        self.marca_comercial = marca_comercial
        self.modelo_comercial = modelo_comercial
        self.descripcion = descripcion



    def guardar(self):

        sql = '''
        INSERT INTO modelos 
            (marca_fabricante, modelo_fabricante, 
             marca_comercial, modelo_comercial,
             descripcion)
        VALUES (%s, %s, %s, %s, %s)'''

        datos = (
            self.marca_fabricante,
            self.modelo_fabricante,
            self.marca_comercial,
            self.modelo_comercial,
            self.descripcion
        )

        self.ejecutar_query(sql, datos)

    @staticmethod
    def listar():

        sql = '''
        SELECT 
            id_modelo, 
            marca_comercial, 
            modelo_comercial 
        FROM modelos
        ORDER BY marca_comercial, modelo_comercial
        '''

        conexion = Modelo()
        return conexion.ejecutar_query(sql, fetch=True)

    @staticmethod
    def obtener_reporte(id_mantenimiento):

        conexion = Mantenimiento()

        sql = '''
        SELECT archivo_reporte,
        FROM  mantenimientos
        WHERE id_mantenimiento = %s
        '''

        resultado = conexion.ejecutar_query(sql, (id_mantenimiento,))

        return resultado[0][0] if resultado else None
