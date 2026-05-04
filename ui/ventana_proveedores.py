import tkinter as tk
from tkinter import messagebox, ttk

from models.proveedor import Proveedor
from utils.exportar_excel import exportar_treeview


class VentanaProveedor:

    def __init__(self, root):

        self.root = tk.Toplevel(root)
        self.root.title('Proveedores')
        self.root.geometry('1500x700')
        self.centrar_ventana()

        tk.Label(self.root, text='Nombre').pack()
        self.nombre = tk.Entry(self.root)
        self.nombre.pack()

        tk.Label(self.root, text='Direccion').pack()
        self.direccion = tk.Entry(self.root)
        self.direccion.pack()

        tk.Label(self.root, text='Correo').pack()
        self.correo = tk.Entry(self.root)
        self.correo.pack()

        tk.Label(self.root, text='Pagina').pack()
        self.pagina = tk.Entry(self.root)
        self.pagina.pack()

        tk.Label(self.root, text='Entidad').pack()
        self.entidad = tk.Entry(self.root)
        self.entidad.pack()

        tk.Label(self.root, text='Clasificiacion').pack()
        self.clasificacion = ttk.Combobox(
            self.root,
            values=['INFRAESTRUCTURA', 'SERVICIOS', 'HARDWARE', 'SOFTWARE', 'REDES', 'OBRA CIVIL']
            )
        self.clasificacion.pack()

        tk.Button(
            self.root,
            text='Guardar',
            command=self.guardar
            ).pack(pady=10)

        self.tabla = ttk.Treeview(
            self.root,
            columns=('ID','Nombre', 'Direccion','Correo', 'Pagina', 'Entidad', 'Clasificacion'),
            show='headings'
        )

        for col in ('ID','Nombre', 'Direccion','Correo', 'Pagina', 'Entidad', 'Clasificacion'):
            self.tabla.heading(col, text=col)

        self.tabla.pack(fill='both', expand=True)

        self.cargar()

        tk.Button(
            self.root,
            text='📥 Exportar TODO',
            command=lambda: exportar_treeview(self.tabla)
        ).pack(pady=5)

        tk.Button(
            self.root,
            text='🗃️ Exportar Seleccionado',
            command=lambda: exportar_treeview(self.tabla, True)
        ).pack(pady=5)

    def guardar(self):

        nombre = self.nombre.get().strip()
        direccion = self.direccion.get().strip()
        correo = self.correo.get().strip()
        pagina = self.pagina.get().strip()
        entidad = self.entidad.get().strip()
        clasificacion = self.clasificacion.get().strip()

        if not nombre or not clasificacion:
            messagebox.showwarning('Aviso', 'Campos obligatorios')
            return

        Proveedor.crear(nombre, direccion, correo, pagina, entidad, clasificacion)

        messagebox.showinfo('OK', 'Proveedor guardado correctamente')

        self.cargar()

    def cargar(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for p in Proveedor.listar():
            self.tabla.insert('','end', values=(p[0], p[1], p[2] ,p[3], p[4], p[5], p[6]))

    def centrar_ventana(self):

        self.root.update_idletasks()

        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()

        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)

        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
