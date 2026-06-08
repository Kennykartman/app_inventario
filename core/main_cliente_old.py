import tkinter as tk
from core.config_manager import cargar_config
from ui.login import VentanaLogin
from ui.config_server import  ConfigServidor

root = tk.Tk()

config = cargar_config()

# si no hay config (Pide datos)
if not config or not config.get('host'):
    ConfigServidor(root)
else:
    VentanaLogin(root)

root.mainloop()