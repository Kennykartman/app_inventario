from models.base_model import BaseModel
from utils.security import hash_password

class Usuario(BaseModel):

    @staticmethod
    def validar(username, password):

        conexion = Usuario()

        sql = '''
        SELECT id_usuario, username, password, rol, primer_login
        FROM usuarios
        WHERE username = %s
        '''

        resultado = conexion.ejecutar_query(
            sql,
            (username,),
            fetch=True
        )

        if not resultado:
            return None

        user = resultado[0]

        if user[3] == 'NOTIFICACION':
            return None

        pwd_hash = hash_password(password)

        if user[2] != pwd_hash:
            return None

        return user

    @staticmethod
    def crear(username, password, rol, email):

        conexion = Usuario()

        # Regla de seguridad
        if rol != "NOTIFICACION" and not password:
            raise ValueError('Password requerido para este rol')

        if password:
            pwd_hash = hash_password(password)
        else:
            pwd_hash = None

        sql = '''
        INSERT INTO usuarios (username, password, rol, email, primer_login, activo)
        VALUES (%s, %s, %s, %s, TRUE, TRUE)
        '''

        #print(sql)
        #print((username, pwd_hash, rol, email))
        conexion.ejecutar_query(sql, (username, pwd_hash, rol, email))

    @staticmethod
    def listar():

        conexion = Usuario()

        sql = '''
        SELECT id_usuario,
               username, 
               rol, 
               email
        FROM usuarios
        ORDER BY id_usuario
        '''

        return conexion.ejecutar_query(sql, fetch=True)

    @staticmethod
    def actualizar_password(id_usuario, nueva_password):

        conexion = Usuario()

        pwd_hash = hash_password(nueva_password)

        sql = '''
        UPDATE usuarios
        SET password = %s,
            primer_login = FALSE
        WHERE id_usuario = %s
        '''

        conexion.ejecutar_query(sql, (pwd_hash, id_usuario))

    @staticmethod
    def obtener_email():

        conexion = Usuario()

        sql = '''
        SELECT email
        FROM usuarios
        WHERE rol IN ('ADMIN', 'OPERADOR', 'NOTIFICACION')
        '''

        resultado = conexion.ejecutar_query(sql, fetch=True)

        return [r[0] for r in resultado if r[0]]

    @staticmethod
    def listar_tecnicos():

        conexion = Usuario()

        sql = '''
        SELECT id_usuario, username
        FROM usuarios
        WHERE rol = 'OPERADOR'
        '''

        return conexion.ejecutar_query(sql, fetch=True)

