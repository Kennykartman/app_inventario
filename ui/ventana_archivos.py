import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from utils.rutas import obtener_ruta_archivos
import shutil
import os

from models.asignacion import Asignacion



class VentanaArchivos:

    def __init__(self, root, id_asignacion):

        self.id_asignacion = id_asignacion

        self.root = tk.Toplevel(root)
        self.root.title('Archivos de instalacion')
        self.root.geometry('700x400')

        # Tabla
        self.tabla = ttk.Treeview(
            self.root,
            columns=('ID', 'Archivo', 'Ruta'),
            show='headings',
        )

        self.tabla.heading('ID', text='ID')
        self.tabla.heading('Archivo', text='Archivo')
        self.tabla.heading('Ruta', text='Archivo')

        self.tabla.pack(fill='both', expand=True)

        # Botones
        tk.Button(self.root, text='Subir archivo', command=self.subir).pack()
        tk.Button(self.root, text='Abrir', command=self.abrir).pack()

        self.cargar()

    def subir(self):

            ruta = filedialog.askopenfilename()

            if not ruta:
                return

            carpeta = obtener_ruta_archivos('Asignaciones')

            if not os.path.exists(carpeta):
                os.makedirs(carpeta)

            nombre = os.path.basename(ruta)
            destino = os.path.join(carpeta,
                                   f'{self.id_asignacion}_{nombre}'
                                   )

            shutil.copy(ruta, destino)

            Asignacion.guardar_archivo(self.id_asignacion, destino)

            self.cargar()

    def cargar(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        archivos = Asignacion.obtener_archivos(self.id_asignacion)

        for a in archivos:
            id_archivo = a[0]
            ruta = a[1]

            nombre = os.path.basename(ruta)

            self.tabla.insert(
                '',
                'end',
                values=(id_archivo, nombre, ruta)
            )

    def abrir(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            return

        datos = self.tabla.item(seleccionado)['values']
        ruta = datos[2]

        if os.path.exists(ruta):
            os.startfile(ruta)

        else:
            messagebox.showerror('Error', 'Archivo no encontrado')
