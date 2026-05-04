import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from models.asignacion import Asignacion
from models.cliente import Cliente
from utils.exportar_excel import exportar_treeview

class VentanaClienteEquipos:

    def __init__(self, parent):

        self.root = tk.Toplevel(parent)
        self.root.title('Equipos - Clientes')
        self.root.geometry('1000x400')

        # Clientes
        tk.Label(self.root, text='Cliente').pack()

        self.clientes = Cliente.listar()

        self.cliente_var = tk.StringVar()

        cliente_text = [c[1] for c in self.clientes]

        self.combo_cliente = ttk.Combobox(
            self.root,
            textvariable=self.cliente_var,
            values=cliente_text
        )
        self.combo_cliente.pack()

        tk.Button(
            self.root,
            text='Ver equipos',
            command=self.cargar_equipos
        ).pack(pady=10)

        # Tabla
        self.tabla = ttk.Treeview(
            self.root,
            columns=('Serie', 'Marca', 'Modelo', 'Ubicacion', 'Fecha'),
            show='headings'
        )

        self.tabla.heading('Serie', text='Serie')
        self.tabla.heading('Marca', text='Marca')
        self.tabla.heading('Modelo', text='Modelo')
        self.tabla.heading('Ubicacion', text='Ubicacion')
        self.tabla.heading('Fecha', text='Fecha')

        self.tabla.pack(fill='both', expand=True)

        tk.Button(
            self.root,
            text='📥 Exportar TODO',
            command=lambda: exportar_treeview(self.tabla)
        ).pack(pady=5)

        # Funcion cargar

    def cargar_equipos(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        index = self.combo_cliente.current()

        if index == -1:
            messagebox.showwarning('Aviso', 'Selecciona un cliente')
            return

        id_cliente = self.clientes[index][0]

        equipos = Asignacion.listar_por_cliente(id_cliente)

        for e in equipos:
            self.tabla.insert('', 'end', values=e)
