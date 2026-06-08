import tkinter as tk

from core.config_manager import cargar_config
from ui.config_server import ConfigServidor
from ui.login import VentanaLogin

root = tk.Tk()

config = cargar_config()

if not config or not config.get('host'):
    ConfigServidor(root)
else:
    VentanaLogin(root)

root.mainloop()