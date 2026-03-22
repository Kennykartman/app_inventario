import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

from models.asignacion import Asignacion
from models.equipo import Equipo
from models.cliente import Cliente


class VentanaAsignacion:

    def __init__(self, parent):

        self.root = tk.Toplevel(parent)
        self.root.title('Asignar equipo a cliente')
        self.root.geometry('1000x600')

        # Equipos
        tk.Label(self.root, text='Equipo').pack()

        self.equipos = Equipo.listar_disponibles()

        equipos_text = [
            f'{serie} - {marca} {modelo}'
            for _, serie, marca, modelo in self.equipos
        ]

        self.equipo_var = tk.StringVar()

        self.equipo_combo = ttk.Combobox(
            self.root,
            textvariable=self.equipo_var,
            values=equipos_text
        )

        self.equipo_combo.pack()

        # Clientes
        tk.Label(self.root, text='Cliente').pack()

        self.clientes = Cliente.listar()

        clientes_text = [c[1] for c in self.clientes]

        self.cliente_var = tk.StringVar()

        self.cliente_combo = ttk.Combobox(
            self.root,
            textvariable=self.cliente_var,
            values=clientes_text
        )

        self.cliente_combo.pack()

        tk.Label(self.root, text='Ubicacion').pack()

        self.ubicacion = tk.Entry(self.root)

        self.ubicacion.pack()

        # Fecha de asignacion
        tk.Label(self.root, text='Fecha de asignacion').pack()

        self.fecha = DateEntry(
            self.root,
            date_pattern='yyyy-mm-dd'
        )
        self.fecha.pack(pady=5)

        self.fecha.set_date(datetime.now())

        # Boton Asignar
        tk.Button(
            self.root,
            text='Asignar',
            command=self.asignar_equipo
        ).pack(pady=10)

        # Tabla
        self.tabla = ttk.Treeview(
            self.root,
            columns=('ID', 'Equipo', 'Cliente', 'Ubicacion', 'Fecha'),
            show='headings',
        )

        self.tabla.heading('ID', text='ID')
        self.tabla.heading('Equipo', text='Equipo')
        self.tabla.heading('Cliente', text='Cliente')
        self.tabla.heading('Ubicacion', text='Ubicacion')
        self.tabla.heading('Fecha', text='Fecha')

        self.tabla.pack(pady=20, fill='both', expand=True)

        self.cargar_asignaciones()

        tk.Button(
            self.root,
            text="Retirar equipo",
            command=self.retirar_equipo
        ).pack(pady=5)

    def asignar_equipo(self):

        equipo_index = self.equipo_combo.current()
        cliente_index = self.cliente_combo.current()
        ubicacion = self.ubicacion.get()
        fecha = self.fecha.get()

        if equipo_index ==-1 or cliente_index == -1:
            messagebox.showwarning(
                'Aviso',
                'Selecciona equipo y cliente'
            )
            return
        if not fecha:
            messagebox.showwarning('Aviso', 'Selecciona una fecha')
            return

        id_equipo = self.equipos[equipo_index][0]
        id_cliente = self.clientes[cliente_index][0]

        asignacion = Asignacion(
            id_equipo,
            id_cliente,
            ubicacion,
            fecha
        )

        asignacion.guardar()

        self.cargar_asignaciones()
        self.cargar_equipos()

        messagebox.showinfo(
            'Exito',
            'Equipo asignado Correctamente'
        )


    def cargar_asignaciones(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        asignaciones = Asignacion.listar_activas()

        for a in asignaciones:

            self.tabla.insert(
                '',
                'end',
                values=a
            )

    def retirar_equipo(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                'Aviso',
                'Selecciona una asignacion'
            )
            return

        item = seleccionado[0]

        valores = self.tabla.item(item)['values']

        id_asignacion = valores[0]

        Asignacion.cerrar_asignacion(id_asignacion)

        self.cargar_asignaciones()
        self.cargar_equipos()

        messagebox.showinfo(
            'Exito',
            'Equipo retirado correctamente'
        )

    def cargar_equipos(self):

        self.equipos = Equipo.listar_disponibles()

        equipos_text =[
            f'{e[1] if e[1] else 'SIN SERIE'} - {e[2]} {e[3]}'
            for e in self.equipos
        ]

        self.equipo_combo['values'] = equipos_text