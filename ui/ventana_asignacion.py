import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta

from models.asignacion import Asignacion
from models.equipo import Equipo
from models.cliente import Cliente
from models.mantenimiento import Mantenimiento



class VentanaAsignacion:

    def __init__(self, parent):

        self.root = tk.Toplevel(parent)
        self.root.title('Asignar equipo a cliente')
        self.root.geometry('1300x700')
        self.centrar_ventana()



        # Equipos
        tk.Label(self.root, text='Equipo').pack(pady=5)
        self.equipos = Equipo.listar_disponibles()
        equipos_text = [
            f'{serie} - {marca} {modelo}'
            for _, serie, marca, modelo in self.equipos
        ]

        self.equipo_var = tk.StringVar()

        self.equipo_combo = ttk.Combobox(
            self.root,
            textvariable=self.equipo_var,
            values=equipos_text,
            width=40
        )
        self.equipo_combo.pack(pady=5)

        # Clientes
        tk.Label(self.root, text='Cliente').pack()

        self.clientes = Cliente.listar()

        clientes_text = [c[1] for c in self.clientes]

        self.cliente_var = tk.StringVar()

        self.cliente_combo = ttk.Combobox(
            self.root,
            textvariable=self.cliente_var,
            values=clientes_text,
            width=35
        )
        self.cliente_combo.pack()

        tk.Label(self.root, text='Ubicacion').pack(pady=5)
        self.ubicacion = tk.Entry(self.root, width=35)
        self.ubicacion.pack(pady=5)

        # Elegir entre permanente y temporal 04/04/26
        tk.Label(self.root, text='Tipo de asignacion').pack()
        self.tipo_equipo = tk.StringVar()
        self.combo_tipo = ttk.Combobox(
            self.root,
            textvariable=self.tipo_equipo,
            values=['PERMANENTE', 'TEMPORAL'],
            width=30
        )
        self.combo_tipo.pack()

        # Garantia 04/04/26
        tk.Label(self.root, text='Garantia (meses)').pack()
        self.garantia = tk.Entry(self.root)
        self.garantia.pack()


        # Logica dinamica 04/04/26
        def on_tipo_change(event):  # A lo mejor hay un erro en event o self
            if self.tipo_equipo.get() == 'PERMANENTE':
                self.garantia.config(state='normal')
            else:
                self.garantia.delete(0, tk.END)
                self.garantia.config(state='disabled')

        self.combo_tipo.bind('<<ComboboxSelected>>', on_tipo_change)

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
            columns=('ID', 'Serie', 'Equipo', 'Cliente', 'Ubicacion', 'Fecha'),
            show='headings',
        )

        self.tabla.heading('ID', text='ID')
        self.tabla.heading('Serie', text='Numero de Serie')
        self.tabla.heading('Equipo', text='Equipo')
        self.tabla.heading('Cliente', text='Cliente')
        self.tabla.heading('Ubicacion', text='Ubicacion')
        self.tabla.heading('Fecha', text='Fecha')

        self.tabla.pack(pady=20, fill='both', expand=True)

        self.cargar_asignaciones()

        tk.Button(
            self.root,
            text='📎 Archivos',
            command=self.abrir_archivos
        ).pack(pady=5)

        tk.Button(
            self.root,
            text='Retirar equipo',
            command=self.retirar_equipo
        ).pack(pady=5)

        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20, fill='both', expand=True)


    def asignar_equipo(self):

        equipo_index = self.equipo_combo.current()
        cliente_index = self.cliente_combo.current()
        ubicacion = self.ubicacion.get()
        fecha = self.fecha.get()

        # Logica guardar
        tipo = self.tipo_equipo.get()
        fecha_fin_garantia = None

        if tipo == 'PERMANENTE':
            meses = int(self.garantia.get()) if self.garantia.get() else 12

            if meses < 12:
                meses = 12

            fecha_fin_garantia = datetime.now() + timedelta(days=meses * 30)


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
            fecha,
            tipo,
            fecha_fin_garantia
        )

        asignacion.guardar()

        if not Mantenimiento.existe_programado(id_equipo):

            frecuencia = 30

            fecha_programada = datetime.now() + timedelta(days=frecuencia)

            mantenimiento = Mantenimiento(
                id_equipo=id_equipo,
                tipo='PREVENTIVO',
                fecha_programada=fecha_programada.date()
            )

            mantenimiento.guardar()

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

    def obtener_id_asignacion(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning('Aviso',"Selecciona una asignacion")
            return None

        datos = self.tabla.item(seleccionado)['values']
        return datos[0]


    def abrir_archivos(self):

        id_asignacion = self.obtener_id_asignacion()

        if not id_asignacion:
            return

        from ui.ventana_archivos import VentanaArchivos
        VentanaArchivos(self.root, id_asignacion)

    def centrar_ventana(self):

        self.root.update_idletasks()

        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()

        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)

        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
