import tkinter as tk
from tkinter import ttk, messagebox
import os

from models.asignacion import Asignacion


class VentanaArchivosHistorico:

    def __init__(self, root, id_equipo):

        self.root = tk.Toplevel(root)
        self.root.title('Historico de Archivos')
        self.root.geometry('800x400')

        self.id_equipo = id_equipo

        self.tabla = ttk.Treeview(
            self.root,
            columns=('Nombre', 'Tipo de archivo', 'Fecha', 'Ruta'),
            show='headings'
        )

        for col in ('Nombre', 'Tipo de archivo', 'Fecha', 'Ruta'):
            self.tabla.heading(col, text=col)

        self.tabla.column('Ruta', width=0, stretch=False)
        self.tabla.pack(fill='both', expand=True)

        tk.Button(
            self.root,
            text='Abrir archivo',
            command=self.abrir
        ).pack(pady=5)

        self.cargar()

    def cargar(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        archivos = Asignacion.obtener_archivos_por_equipo(self.id_equipo)

        for a in archivos:
            ruta = a[0]
            fecha = a[1]

            if ruta.endswith('.pdf') or ruta.endswith('.txt') or ruta.endswith('.doc') or ruta.endswith('.docx'):
                tipo = 'DOCUMENTO 📄'
            elif ruta.endswith('.jpg') or ruta.endswith('.jpeg') or ruta.endswith('.png'):
                tipo = 'IMAGEN 📷'
            else:
                tipo = 'GENERAL'

            nombre = os.path.basename(ruta)
            self.tabla.insert('', 'end', values=(nombre, tipo, fecha, ruta))

    def abrir(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning('Aviso', 'Selecciona un archivo')
            return

        ruta = self.tabla.item(seleccionado[0])['values'][-1]

        if os.path.exists(ruta):
            os.startfile(ruta)
        else:
            messagebox.showerror('Error', 'Archivo no encontrado')
