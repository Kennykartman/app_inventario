from models.base_model import BaseModel


class Equipo(BaseModel):

    def __init__(self,
                 serie_interna=None,
                 serie_fabricante=None,
                 id_modelo=None,
                 estado='ALMACEN'):

        self.serie_interna = serie_interna
        self.serie_fabricante = serie_fabricante
        self.id_modelo = id_modelo
        self.estado = estado


    def guardar(self):

        sql = """
        INSERT INTO equipos
        (serie_interna, serie_fabricante, id_modelo, estado)
        VALUES (%s, %s, %s, %s)
        """

        datos = (
            self.serie_interna,
            self.serie_fabricante,
            self.id_modelo,
            self.estado
        )

        self.ejecutar_query(sql, datos)

    @staticmethod
    def actualizar_estado(id_equipo, nuevo_estado):

        conexion = Equipo()

        sql = '''
        UPDATE equipos
        SET estado = %s
        WHERE id_equipo = %s
              '''

        datos = (
            nuevo_estado,
            id_equipo
            )

        conexion.ejecutar_query(sql, datos)

    @staticmethod
    def listar():

        conexion = Equipo()

        sql = """
        SELECT
            e.id_equipo,
            e.serie_interna,
            e.serie_fabricante,
            m.marca_comercial,
            m.modelo_comercial,
            e.estado
        FROM equipos e
        JOIN modelos m
            ON e.id_modelo = m.id_modelo
        WHERE e.activo = TRUE
        ORDER BY e.id_equipo
        """

        return conexion.ejecutar_query(sql, fetch=True)

    @staticmethod
    def listar_disponibles():

        conexion = Equipo()

        sql = '''
        SELECT
            e.id_equipo,
            e.serie_interna,
            m.marca_comercial,
            m.modelo_comercial
        FROM equipos e
        JOIN modelos m
            ON e.id_modelo = m.id_modelo
        WHERE e.id_equipo NOT IN (
            SELECT id_equipo
            FROM asignaciones
            WHERE activo = TRUE
        )
        AND e.activo = TRUE
        '''

        return conexion.ejecutar_query(sql, fetch=True)
