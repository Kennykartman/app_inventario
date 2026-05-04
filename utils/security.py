import hashlib
import re


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def validar_password(password):

    if len(password) < 8:
        return False, 'Minimo 8 caracteres'

    if not re.search('[A-Z]', password):
        return False, 'Debe tener una mayuscula'

    if not re.search(r'\d', password):
        return False, 'Debe tener un numero'

    if not re.search(r'[!@#$%^&*]', password):
        return False, 'Debe tener un simbolo'

    return True, 'OK'
