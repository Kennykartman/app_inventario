from models.base_model import BaseModel

class Asignacion(BaseModel):

    def __init__(self, id_equipo=None, id_cliente=None, ubicacion=None, fecha_inicio=None):
        self.id_equipo = id_equipo
        self.id_cliente = id_cliente
        self.ubicacion = ubicacion
        self.fecha_inicio = fecha_inicio

    def guardar(self):

        # 1 Cerrar asginacion anterior
        Asignacion.cerrar_asignacion_activa(self.id_equipo)

        # Insertar nueva
        sql = '''
        INSERT INTO asignaciones
              (id_equipo, id_cliente, fecha_inicio, ubicacion)
              VALUES (%s, %s, %s, %s)
              '''

        datos = (
            self.id_equipo,
            self.id_cliente,
            self.fecha_inicio,
            self.ubicacion
        )

        self.ejecutar_query(sql, datos)

    @staticmethod
    def cerrar_asignacion(id_asignacion):

        conexion = Asignacion()

        sql = '''
        UPDATE asignaciones
        SET 
            fecha_fin = CURRENT_DATE,
            activo = FALSE
        WHERE id_asignacion = %s
        '''

        conexion.ejecutar_query(sql, (id_asignacion,))

    @staticmethod
    def cerrar_asignacion_activa(id_equipo):

        conexion = Asignacion()

        sql = '''
        UPDATE asignaciones
        SET fecha_fin = CURRENT_DATE,
                activo = FALSE
        WHERE id_equipo = %s
        AND activo = TRUE
        '''

        conexion.ejecutar_query(sql, (id_equipo,))

    @staticmethod
    def historial_por_equipo(id_equipo):

        conexion = Asignacion()

        sql = '''
        SELECT
            a.id_asignacion,
            c.nombre,
            a.fecha_inicio,
            a.fecha_fin,
            a.activo,
            a.ubicacion
        FROM asignaciones a
        JOIN clientes c ON a.id_cliente = c.id_cliente
        WHERE a.id_equipo = %s
        ORDER by a.fecha_inicio DESC
        '''

        return conexion.ejecutar_query(sql, (id_equipo,), fetch=True)

    @staticmethod
    def listar_activas():

        conexion = Asignacion()

        sql = '''
        SELECT
            a.id_asignacion,
            e.serie_interna,
            c.nombre,
            a.ubicacion,
            a.fecha_inicio
        FROM asignaciones a
        JOIN equipos e ON a.id_equipo = e.id_equipo
        JOIN clientes c ON a.id_cliente = c.id_cliente
        WHERE a.activo = TRUE
        ORDER BY a.fecha_inicio DESC
        '''

        return conexion.ejecutar_query(sql, fetch=True)

    @staticmethod
    def listar_por_cliente(id_cliente):

        conexion = Asignacion()

        sql = '''
        SELECT
            e.serie_interna,
            m.marca_comercial,
            m.modelo_comercial,
            a.ubicacion,
            a.fecha_inicio
        FROM asignaciones a
        JOIN equipos e ON a.id_equipo = e.id_equipo
        JOIN modelos m ON e.id_modelo = m.id_modelo
        WHERE a.id_cliente = %s
        AND a.activo = TRUE
        ORDER BY a.fecha_inicio DESC
        '''

        return conexion.ejecutar_query(sql, (id_cliente,), fetch=True)
