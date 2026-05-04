import tkinter as tk
from core.config_manager import cargar_config
from ui.config_server import ConfigServidor
from ui.login import VentanaLogin

def iniciar_app():

    config = cargar_config()

    # Primera vez
    if not config:
        root = tk.Tk()
        ConfigServidor(root)
        root.mainloop()

    # Login
    root = tk.Tk()
    VentanaLogin(root)
    root.mainloop()

if __name__ == '__main__':
    iniciar_app()