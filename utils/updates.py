import os
from tkinter import (messagebox)
import logging
from utils.rutas import (obtener_ruta_updates)
from utils.version import (
    obtener_version_local,
    obtener_version_remota,
    obtener_changelog
    )

verificado = False

def verificar_actualizacion():

    global verificado

    if verificado:
        return

    try:
        local = obtener_version_local()
        remota = obtener_version_remota()

        if tuple(
            map(
                int,
                remota.split('.'))
            ) > tuple(
                map(
                    int,
                    local.split('.')
                    )
                    ):

                    respuesta = messagebox.askyesno(
                            'Actualización disponible',
                            f'''
                                    Nueva versión:
                                        {remota}
                                    Actual:
                                        {local}
                                    Cambios:
                                    {obtener_changelog()}
                                    Actualizar?
                                    '''
                                    )
                    if respuesta:
                        ruta_setup = os.path.join(
                            obtener_ruta_updates(),
                            'Humanet_setup.exe')
                        if os.path.exists(ruta_setup):
                            os.startfile(ruta_setup)
                        else:
                            messagebox.showerror(
                                'Error',
                                'No existe instalador')
                    verificado = True
    except Exception as e:

        logging.error(
            f'Error verificando actualizacion:\n{e}',
            exc_info=True
        )