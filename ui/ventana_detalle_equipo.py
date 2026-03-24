import tkinter as tk
from tkinter import ttk

from models.asignacion import Asignacion
from models.mantenimiento import Mantenimiento

class VentanaDetalleEquipo:

    def __init__(self, parent, equipo):

        self.root = tk.Toplevel(parent)
        self.root.title('Detalle del equipo')
        self.root.geometry('1000x700')

        self.equipo = equipo
        self.id_equipo = equipo[0]

        # ===== INFO EQUIPO =====
        tk.Label(self.root, text=f'Serie: {equipo[1]}').pack()
        tk.Label(self.root, text=f'Marca: {equipo[2]}').pack()
        tk.Label(self.root, text=f'Modelo: {equipo[3]}').pack()
        tk.Label(self.root, text=f'Estado: {equipo[4]}').pack()

        # ===== ASIGNACIONES =====
        tk.Label(self.root, text='Asignaciones').pack(pady=10)

        self.tabla_asignaciones = ttk.Treeview(
            self.root,
            columns=('Cliente', 'Inicio', 'Fin', 'Estado', 'Ubicacion'),
            show='headings'
        )

        self.tabla_asignaciones.heading('Cliente', text='Cliente')
        self.tabla_asignaciones.heading('Inicio', text='Inicio')
        self.tabla_asignaciones.heading('Fin', text='Fin')
        self.tabla_asignaciones.heading('Estado', text='Estado')
        self.tabla_asignaciones.heading('Ubicacion', text='Ubicacion')

        self.tabla_asignaciones.pack(fill='both', expand=True)

        self.tabla_asignaciones.tag_configure("activo", background="#d4edda")  # verde claro
        self.tabla_asignaciones.tag_configure("finalizado", background="#f8d7da")  # rojo claro

        # ===== Mantenimientos =====
        tk.Label(self.root, text='Mantenimientos').pack(pady=10)

        self.tabla_mantenimientos = ttk.Treeview(
            self.root,
            columns=('Tipo', 'Fecha', 'Estado'),
            show='headings'
        )

        self.tabla_mantenimientos.heading('Tipo', text='Tipo')
        self.tabla_mantenimientos.heading('Fecha', text='Fecha')
        self.tabla_mantenimientos.heading('Estado', text='Estado')

        self.tabla_mantenimientos.pack(fill='both', expand=True)

        # Cargar datos

        self.cargar_asignaciones()
        self.cargar_mantenimientos()


    def cargar_asignaciones(self):

        for fila in self.tabla_asignaciones.get_children():
            self.tabla_asignaciones.delete(fila)

        historial = Asignacion.historial_por_equipo(self.id_equipo)

        for h in historial:

            estado = 'Activo' if h[4] else 'FINALIZADO'

            tag = 'activo' if h[4] else 'finalizado'

            self.tabla_asignaciones.insert(
                '',
                'end',
                values=(
                    h[1],
                    h[2],
                    h[3] if h[3] else '-',
                    estado,
                    h[5]
                ),
                tags=(tag,)
            )

    def cargar_mantenimientos(self):

        for fila in self.tabla_mantenimientos.get_children():
            self.tabla_mantenimientos.delete(fila)

        mantenimientos = Mantenimiento.listar_por_equipo(self.id_equipo)

        for m in mantenimientos:

            self.tabla_mantenimientos.insert(
                '',
                'end',
                values=m
            )
