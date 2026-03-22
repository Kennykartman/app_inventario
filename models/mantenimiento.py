from models.base_model import BaseModel

class Mantenimiento(BaseModel):

    def __init__(self,
                 id_equipo=None,
                 tipo=None,
                 fecha_programada=None,
                 descripcion=None,
                 tecnico=None):

        self.id_equipo = id_equipo
        self.tipo = tipo
        self.fecha_programada = fecha_programada
        self.descripcion = descripcion
        self.tecnico = tecnico

    def guardar(self):

        sql = '''
        INSERT INTO mantenimientos
        (id_equipo, tipo, fecha_programada, descripcion, tecnico)
        VALUES (%s, %s, %s, %s, %s)
        '''

        datos = (
            self.id_equipo,
            self.tipo,
            self.fecha_programada,
            self.descripcion,
            self.tecnico
        )

        self.ejecutar_query(sql, datos)

    @staticmethod
    def listar():

        conexion = Mantenimiento()

        sql = '''
        SELECT
            M.id_mantenimiento,
            e.serie_interna,
            m.tipo,
            m.fecha_programada,
            m.fecha_realizada,
            m.estado
        FROM mantenimientos m
        JOIN equipos e 
            ON m.id_equipo = e.id_equipo
        ORDER BY m.fecha_programada DESC
        '''

        return conexion.ejecutar_query(sql, fetch=True)

    @staticmethod
    def completar(id_mantenimiento):

        conexion = Mantenimiento()

        sql = '''
        UPDATE mantenimientos
        SET
            fecha_realizada = CURRENT_DATE,
            estado = 'REALIZADO'
        WHERE id_mantenimiento = %s
        '''

        conexion.ejecutar_query(sql, (id_mantenimiento,))
