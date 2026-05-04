import tkinter as tk
from tkinter import messagebox

class ConfigServidor:

    def __init__(self, root):

        self.root = root
        self.root.title('Configurar Servidor')
        self.root.geometry('300x250')

        tk.Label(root, text='IP Servidor').pack()
        self.host = tk.Entry(root)
        self.host.pack()

        tk.Label(root, text='Base de datos').pack()
        self.db = tk.Entry(root)
        self.db.pack()

        tk.Label(root, text='Usuario').pack()
        self.user = tk.Entry(root)
        self.user.pack()

        tk.Label(root, text='Password').pack()
        self.password = tk.Entry(root, show='*')
        self.password.pack()

        tk.Label(root, text='Puerto').pack()
        self.port = tk.Entry(root)
        self.port.insert(0, "5432") # defualt
        self.port.pack()

        tk.Button(
            root,
            text='Guardar',
            command=self.guardar
        ).pack(pady=10)

    def guardar(self):

        data = {'host': self.host.get(),
                'database': self.db.get(),
                'user': self.user.get(),
                'password': self.password.get(),
                'port': self.port.get()}

        # Solo si conecta guarda
        from core.config_manager import guardar_config
        guardar_config(data)

        messagebox.showinfo('Ok', 'Configuracion guardada correctamente')
        self.root.destroy()