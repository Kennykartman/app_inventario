import tkinter as tk
from core.config_manager import guardar_config
from ui.login import VentanaLogin

# Config fija de servidor
config = {
    "modo": "cliente",
    "host": "localhost",
    "database": "inventario_tecnico",
    "user": "postgres",
    "password": "Temporal-25",
    "port": "5433",

    "ruta_archivos": "\\localhost\\archiver"
}

guardar_config(config)

root = tk.Tk()
VentanaLogin(root)
root.mainloop()