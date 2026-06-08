import tkinter as tk
from tkinter import messagebox, filedialog
from utils.estilos import *


class ConfigServidor:

    def __init__(self, root):

        self.root = root
        self.root.title('Config Server')
        self.root.geometry('500x450')

        tk.Label(root,
                 bg=COLOR_BG,
                 fg=COLOR_TEXTO_MAGE,
                 text='db Server: ').pack()
        self.host = tk.Entry(root)
        self.host.pack()

        tk.Label(root,
                 bg=COLOR_BG,
                 fg=COLOR_TEXTO_MAGE,
                 text='db Name: ').pack()
        self.db = tk.Entry(root)
        self.db.pack()

        tk.Label(root,
                 bg=COLOR_BG,
                 fg=COLOR_TEXTO_MAGE,
                 text='db User: ').pack()
        self.user = tk.Entry(root)
        self.user.pack()

        tk.Label(root,
                 bg=COLOR_BG,
                 fg=COLOR_TEXTO_MAGE,
                 text='db Password: ').pack()
        self.password = tk.Entry(root, show='*')
        self.password.pack()

        tk.Label(root,
                 bg=COLOR_BG,
                 fg=COLOR_TEXTO_MAGE,
                 text='db Port: ').pack()
        self.port = tk.Entry(root)
        self.port.insert(0, "5432") # defualt
        self.port.pack()

        #### Boton de ruta de almacenamiento ####
        tk.Label(
            root,
            bg=COLOR_BG,
            fg=COLOR_TEXTO_MAGE,
            text='Archiver'
        ).pack()
        self.ruta = tk.Entry(
            root,
            width=40
        )
        self.ruta.pack()
        tk.Button(
            root,
            bg=COLOR_PRIMARIO,
            fg=COLOR_TEXTO,
            font=FUENTE_BOTON,
            text='Carpeta de almacenamiento',
            command=self.buscar_ruta_archiver
        ).pack(pady=5)
        ##########################

        #### Boton de ruta de actualizaciones ####
        tk.Label(
            root,
            bg=COLOR_BG,
            fg=COLOR_TEXTO_MAGE,
            text='Updates'
        ).pack()
        self.ruta_updates = tk.Entry(
            root,
            width=40
        )
        self.ruta_updates.pack()
        tk.Button(
            root,
            bg=COLOR_PRIMARIO,
            fg=COLOR_TEXTO,
            font= FUENTE_BOTON,
            text='Carpeta de actualizaciones',
            command=self.buscar_ruta_update
        ).pack(pady=5)
        #########################

        tk.Button(
            root,
            fg=COLOR_TEXTO,
            font=FUENTE_BOTON,
            text='Guardar',
            command=self.guardar
        ).pack(pady=10)

    def guardar(self):

        data = {'host': self.host.get(),
                'database': self.db.get(),
                'user': self.user.get(),
                'password': self.password.get(),
                'port': self.port.get(),
                "ruta_archivos": self.ruta.get(),
                "ruta_updates": self.ruta_updates.get()
                }

        from core.config_manager import CONFIG_FILE

        messagebox.showinfo(
            'ruta',
            CONFIG_FILE
        )

        # Solo si conecta guarda
        from core.config_manager import guardar_config
        guardar_config(data)

        messagebox.showinfo('Ok', 'Configuracion guardada correctamente')
        self.root.destroy()

    def buscar_ruta_archiver(self):

        ruta = filedialog.askdirectory(
            title='Seleccionar carpeta de almacenamiento'
        )

        if ruta:
            self.ruta.delete(0, tk.END)
            self.ruta.insert(0, ruta)

    def buscar_ruta_update(self):

        ruta_updates = filedialog.askdirectory(
            title='Seleccionar carpeta de actualizaciones'
        )

        if ruta_updates:
            self.ruta_updates.delete(0, tk.END)
            self.ruta_updates.insert(0, ruta_updates)
