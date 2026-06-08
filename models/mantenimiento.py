from core.config import conectar
from models.base_model import BaseModel

class Mantenimiento(BaseModel):

    def __init__(self,
                 id_equipo=None,
                 tipo=None,
                 fecha_programada=None,
                 descripcion=None,
                 tecnico=None,
                 estado="PENDIENTE",
                 ):

        self.id_equipo = id_equipo
        self.tipo = tipo
        self.fecha_programada = fecha_programada
        self.descripcion = descripcion
        self.tecnico = tecnico
        self.estado = estado

    def guardar(self):

        sql = '''
        INSERT INTO mantenimientos
        (id_equipo, tipo, fecha_programada, descripcion, tecnico, estado)
        VALUES (%s, %s, %s, %s, %s, %s)
        '''

        datos = (
            self.id_equipo,
            self.tipo,
            self.fecha_programada,
            self.descripcion,
            self.tecnico,
            self.estado
        )

        self.ejecutar_query(sql, datos)

    @staticmethod
    def listar():

        conexion = Mantenimiento()

        sql = '''
        SELECT
            m.id_mantenimiento,
            e.serie_interna,
            mo.marca_comercial,
            mo.modelo_comercial,
            m.tipo,
            m.fecha_programada,
            m.fecha_realizada,
            m.estado,
            m.archivo_reporte,
            m.archivo_diagnostico
        FROM mantenimientos m
        JOIN equipos e ON m.id_equipo = e.id_equipo
        JOIN modelos mo ON e.id_modelo = mo.id_modelo
        ORDER BY m.fecha_programada DESC
        '''

        return conexion.ejecutar_query(sql, fetch=True)

    @staticmethod
    def completar(id_mantenimiento, solucion):

        conexion = Mantenimiento()

        sql = '''
        UPDATE mantenimientos
        SET
            fecha_realizada = CURRENT_DATE,
            estado = 'REALIZADO',
            solucion = %s
        WHERE id_mantenimiento = %s
        '''

        conexion.ejecutar_query(sql, (solucion, id_mantenimiento,))

    @staticmethod
    def listar_por_equipo(id_equipo):

        conexion = Mantenimiento()

        sql = '''
        SELECT
            tipo,
            fecha_programada,
            estado
        FROM mantenimientos
        WHERE id_equipo = %s
        ORDER BY fecha_programada DESC
        '''

        return conexion.ejecutar_query(sql, (id_equipo,), fetch=True)

    @staticmethod
    def proximos_mantenimientos():

        conexion = Mantenimiento()

        sql = '''
        SELECT
            m.id_mantenimiento,
            e.serie_interna,
            m.fecha_programada
        FROM mantenimientos m
        JOIN equipos e ON m.id_equipo = e.id_equipo
        WHERE m.estado = 'PENDIENTE'
        AND m.fecha_programada <= CURRENT_DATE + INTERVAL '3 days'
        ORDER BY m.fecha_programada
        '''
        return conexion.ejecutar_query(sql, fetch=True)

    @staticmethod
    def existe_programado(id_equipo):

        conexion = Mantenimiento()
        sql = '''
        SELECT COUNT(*)
        FROM mantenimientos
        WHERE id_equipo = %s
        AND estado = 'PENDIENTE'
        AND fecha_programada >= CURRENT_DATE
        '''

        resultado = conexion.ejecutar_query(sql, (id_equipo,), fetch=True)

        return resultado[0][0] > 0

    @staticmethod
    def guardar_reporte(id_mantenimiento, ruta):

        conexion = Mantenimiento()

        sql = '''
        UPDATE mantenimientos
        SET archivo_reporte = %s
        WHERE id_mantenimiento = %s
        '''

        conexion.ejecutar_query(sql, (ruta, id_mantenimiento,))

    @staticmethod
    def obtener_reporte(id_mantenimiento):

        conexion = Mantenimiento()

        sql = '''
        SELECT archivo_reporte
        FROM mantenimientos
        WHERE id_mantenimiento = %s
        '''
        resultado = conexion.ejecutar_query(sql, (id_mantenimiento,), fetch=True)

        return resultado[0][0] if resultado else None

    @staticmethod
    def guardar_diagnostico(id_mantenimiento, diagnostico):

        conexion = Mantenimiento()

        sql = '''
        UPDATE mantenimientos
        SET diagnostico = %s
        WHERE id_mantenimiento = %s
        '''

        conexion.ejecutar_query(sql, (diagnostico, id_mantenimiento,))

    @staticmethod
    def actualizar_tipo(id_mantenimiento, tipo):

        conexion = Mantenimiento()

        sql = '''
        UPDATE mantenimientos
        SET tipo = %s
        WHERE id_mantenimiento = %s
        '''

        conexion.ejecutar_query(sql, (tipo, id_mantenimiento))

    @staticmethod
    def guardar_archivo_diagnostico(id_mantenimiento, ruta):

        conexion = Mantenimiento()

        sql = '''
        UPDATE mantenimientos
        SET archivo_diagnostico = %s
        WHERE id_mantenimiento = %s
        '''

        conexion.ejecutar_query(sql, (ruta, id_mantenimiento,))

    @staticmethod
    def obtener_archivo_diagnostico(id_mantenimiento):

        conexion = Mantenimiento()

        sql = '''
        SELECT archivo_diagnostico
        FROM mantenimientos
        WHERE id_mantenimiento = %s
        '''

        resultado = conexion.ejecutar_query(sql, (id_mantenimiento,), fetch=True)

        return resultado[0][0] if resultado else None

    @staticmethod
    def contar_pendientes():

        conexion = Mantenimiento()

        sql = '''
        SELECT COUNT(*)
        FROM mantenimientos
        WHERE estado = 'PENDIENTE'
        '''

        resultado = conexion.ejecutar_query(sql, fetch=True)

        return resultado[0][0]

    @staticmethod
    def contar_vencidos():

        conexion = Mantenimiento()

        sql = '''
        SELECT COUNT(*)
        FROM mantenimientos
        WHERE estado = 'PENDIENTE'
        AND fecha_programada < CURRENT_DATE
        '''

        resultado = conexion.ejecutar_query(sql, fetch=True)

        return resultado[0][0]

    @staticmethod
    def mantenimientos_por_tecnico():

        conexion = Mantenimiento()

        sql = '''
        SELECT tecnico, COUNT(*)
        FROM mantenimientos
        WHERE estado = 'PENDIENTE'
        GROUP BY tecnico
        ORDER BY COUNT(*) DESC
        '''

        return conexion.ejecutar_query(sql, fetch=True)

    @staticmethod
    def obtener_info(id_mantenimiento):

        conexion = Mantenimiento()

        sql = '''
        SELECT 
            m.descripcion, 
            m.diagnostico, 
            m.solucion,
            
            e.serie_interna,
            
            c.nombre,
            
            m.tipo,
            m.fecha_programada,
            m.estado,
            m.tecnico,
            
            m.archivo_diagnostico,
            m.archivo_reporte
            
        FROM mantenimientos m
        JOIN equipos e
            ON m.id_equipo = e.id_equipo
        LEFT JOIN asignaciones a
            ON e.id_equipo = a.id_equipo
            AND a.activo = TRUE
        LEFT JOIN clientes c
            ON a.id_cliente = c.id_cliente
        WHERE M.id_mantenimiento = %s
        '''
        resultado = conexion.ejecutar_query(sql, (id_mantenimiento,), fetch=True)
        return resultado[0]

    @staticmethod
    def agregar_comentario(id_mantenimiento, comentario):

        conexion = Mantenimiento()

        sql = '''
        INSERT INTO comentarios_mantenimiento
              (id_mantenimiento, comentario
              )
              VALUES (%s, %s)
              '''
        conexion.ejecutar_query(sql, (id_mantenimiento, comentario,))

        sql_update = '''
        UPDATE mantenimientos
        SET ultima_actualizacion = NOW()
            WHERE id_mantenimiento = %s
        '''

        conexion.ejecutar_query(sql_update, (id_mantenimiento,))

    @staticmethod
    def obtener_comentarios(id_mantenimiento):

        conexion = Mantenimiento()

        sql = '''
        SELECT 
            comentario,
            fecha
        FROM comentarios_mantenimiento
            WHERE id_mantenimiento = %s
            ORDER BY fecha DESC
        '''

        return conexion.ejecutar_query(sql, (id_mantenimiento,), fetch=True)