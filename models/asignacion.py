from models.base_model import BaseModel

class Asignacion(BaseModel):

    def __init__(self, id_equipo=None,
                 id_cliente=None,
                 ubicacion=None,
                 fecha_inicio=None,
                 tipo_quipo=None,
                 fecha_fin_garantia=None):
        self.id_equipo = id_equipo
        self.id_cliente = id_cliente
        self.ubicacion = ubicacion
        self.fecha_inicio = fecha_inicio
        self.tipo_equipo = tipo_quipo
        self.fecha_fin_garantia = fecha_fin_garantia

    def guardar(self):

        # 1 Cerrar asginacion anterior
        Asignacion.cerrar_asignacion_activa(self.id_equipo)

        # Insertar nueva
        sql = '''
        INSERT INTO asignaciones
              (id_equipo, id_cliente, fecha_inicio, ubicacion, tipo_equipo, fecha_fin_garantia)
              VALUES (%s, %s, %s, %s, %s, %s)
              '''

        datos = (
            self.id_equipo,
            self.id_cliente,
            self.fecha_inicio,
            self.ubicacion,
            self.tipo_equipo,
            self.fecha_fin_garantia
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

    @staticmethod
    def guardar_archivo(id_asignacion, ruta):

        conexion = Asignacion()

        sql = '''
        INSERT INTO archivo_asignacion (id_asignacion, ruta)
        VALUES (%s, %s)
        '''

        conexion.ejecutar_query(sql,(id_asignacion, ruta))

    @staticmethod
    def obtener_archivos(id_asignacion):

        conexion = Asignacion()

        sql = '''
        SELECT id_archivo, ruta
        FROM archivo_asignacion
        WHERE id_asignacion = %s
        '''

        return conexion.ejecutar_query(sql, (id_asignacion,), fetch=True)

    @staticmethod
    def obtener_archivos_por_equipo(id_equipo):

        conexion = Asignacion()

        sql = '''
        SELECT a.ruta, a.fecha        
        FROM archivo_asignacion a 
        JOIN asignaciones s
            ON a.id_asignacion = s.id_asignacion
        WHERE s.id_equipo = %s
        ORDER BY a.id_archivo DESC
        '''

        return conexion.ejecutar_query(sql, (id_equipo,), fetch=True)
