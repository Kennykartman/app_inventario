import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from psycopg2 import errors

from models.asignacion import Asignacion
from models.equipo import Equipo
from models.modelo import Modelo
from ui.ventana_detalle_equipo import VentanaDetalleEquipo



class VentanaEquipo:

    def __init__(self, parent):

        self.root = tk.Toplevel(parent)
        self.root.title("Registro de Equipos")
        self.root.geometry("1100x800")

        # Serie interna
        tk.Label(self.root, text="Serie Interna").pack()
        self.serie_interna = tk.Entry(self.root)
        self.serie_interna.pack()

        # Serie fabricante
        tk.Label(self.root, text="Serie Fabricante").pack()
        self.serie_fabricante = tk.Entry(self.root)
        self.serie_fabricante.pack()

        # Modelo
        tk.Label(self.root, text="Modelo").pack()

        self.modelos = Modelo.listar()

        self.modelo_var = tk.StringVar()

        modelos_text = [f"{m[1]} {m[2]}" for m in self.modelos]

        self.modelo_combo = ttk.Combobox(
            self.root,
            textvariable=self.modelo_var,
            values=modelos_text
        )

        self.modelo_combo.pack()

        # Estado
        tk.Label(self.root, text="Estado").pack()

        self.estado = tk.StringVar(value="ALMACEN")

        estados = ["ALMACEN", "INSTALADO", "REPARACION", "BAJA"]

        self.estado_menu = ttk.Combobox(
            self.root,
            textvariable=self.estado,
            values=estados
        )

        self.estado_menu.pack()

        # Botón guardar
        tk.Button(
            self.root,
            text="Guardar",
            command=self.guardar_equipo
        ).pack(pady=10)

        tk.Label(self.root, text='Buscar equipo').pack()

        self.busqueda= tk.Entry(self.root)
        self.busqueda.pack()

        self.busqueda.bind('<KeyRelease>', self.buscar_equipo)

        # TABLA

        tk.Label(
            self.root,
            text='Equipos registrados en almacen',
            font=('Arial',12,'bold')
        ).pack(pady=10)

        self.tabla = ttk.Treeview(
            self.root,
            columns=('ID', "Serie", 'Marca', "Modelo", "Estado"),
            show="headings"
        )

        self.tabla.heading('ID', text='ID')
        self.tabla.heading("Serie", text="Serie Interna")
        self.tabla.heading("Marca", text="Marca")
        self.tabla.heading("Modelo", text="Modelo")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.tag_configure('ALMACEN', background='#d0e7ff')
        self.tabla.tag_configure('INSTALADO', background='#d4f7d4')
        self.tabla.tag_configure('REPARACION', background='#fff3dc')
        self.tabla.tag_configure('BAJA', background='#f8d7da')

        self.tabla.pack(pady=20, fill='both', expand=True)

        # cargar datos
        self.cargar_equipos()

        tk.Button(
            self.root,
            text='Instalar',
            command=lambda: self.cambiar_estado('INSTALADO')
        ).pack()

        tk.Button(
            self.root,
            text='Reparacion',
            command=lambda: self.cambiar_estado('REPARACION')
        ).pack()

        tk.Button(
            self.root,
            text="Dar de baja",
            command=lambda: self.cambiar_estado("BAJA")
        ).pack()

        tk.Button(
            self.root,
            text='Regresar a almacen',
            command=lambda: self.cambiar_estado("ALMACEN")
        ).pack()

        # Historial

        tk.Button(
            self.root,
            text='Ver historial',
            command=self.ver_historial
        ).pack(pady=5)

        tk.Button(
            self.root,
            text='Ver detalle',
            command=self.ver_detalle
        ).pack()

    def cambiar_estado(self, nuevo_estado):

        equipo = self.obtener_equipo_seleccionado()

        if not equipo:
            messagebox.showwarning(
                'Aviso',
                'Selecciona un equipo primero'
            )
            return

        id_equipo = equipo[0]

        Equipo.actualizar_estado(id_equipo, nuevo_estado)

        self.cargar_equipos()

        messagebox.showinfo(
            'Exito',
            f'Estado cambiado a {nuevo_estado}'
        )

        estado_actual = equipo[4]

        if estado_actual == 'BAJA':
            messagebox.showwarning(
                'Aviso',
                'Este equipo ya fue dado de baja'
            )
            return

    def obtener_equipo_seleccionado(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            return None

        item = seleccionado[0]

        valores = self.tabla.item(item)["values"]

        return valores

    def cargar_equipos(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        equipos = Equipo.listar()

        for e in equipos:

            marca = f'{e[3]}'
            modelo = f"{e[4]}"
            estado = e[5]

            self.tabla.insert(
                "",
                "end",
                values=(
                    e[0],      # id_equipo
                    e[1],      # serie interna
                    marca,     # modelo interno
                    modelo,    # modelo
                    estado     # estado
                ),
                tags=(estado,)
            )


    def guardar_equipo(self):

        serie_int = self.serie_interna.get()
        serie_fab = self.serie_fabricante.get()
        estado = self.estado.get()

        indice = self.modelo_combo.current()
        if indice == -1:
            messagebox.showwarning(
                'aviso',
                'Seleccionar un modelo'
            )
            return

        id_modelo = self.modelos[indice][0]

        equipo = Equipo(
            serie_int,
            serie_fab,
            id_modelo,
            estado
        )

        try:
            equipo.guardar()

            self.cargar_equipos()

            messagebox.showinfo("Éxito",
                                "Equipo guardado correctamente"
                                )
        except errors.UniqueViolation:

            messagebox.showerror("error",
                                 'El numero de serie del equipo ya existe'
                                 )
        except Exception as e:

            messagebox.showerror("error",
                                 f'Ocurrio un problema:\n{e}'
                                 )

    def buscar_equipo(self, event):

        texto = self.busqueda.get().lower()

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        equipos = Equipo.listar()

        for e in equipos:

            if texto in str(e[1]).lower():

                marca = e[3]
                modelo = e[4]

                self.tabla.insert(
                    "",
                    "end",
                    values=(
                        e[0],
                        e[1],
                        marca,
                        modelo,
                        e[5]
                    )
                )

    def ver_historial(self):

        equipo = self.obtener_equipo_seleccionado()

        if not equipo:
            messagebox.showwarning('Aviso','Selecciona un equipo')
            return

        id_equipo = equipo[0]

        historial = Asignacion.historial_por_equipo(id_equipo)

        ventana = tk.Toplevel(self.root)
        ventana.title('Historial de asignaciones')
        ventana.geometry('900x400')

        tabla = ttk.Treeview(
            ventana,
            columns=('Cliente', 'Inicio', 'Fin', 'Estado', 'Ubicacion'),
            show='headings',
        )

        tabla.heading('Cliente', text='Cliente')
        tabla.heading('Inicio', text='Fecha inicio')
        tabla.heading('Fin', text='Fecha fin')
        tabla.heading('Estado', text='Estado')
        tabla.heading('Ubicacion', text='Ubicacion')

        tabla.pack(fill='both', expand=True)

        for h in historial:

            estado = 'ACTIVO' if h[4] else 'FINALIZADO'

            tabla.insert(
                '',
                "end",
                values=(
                    h[1],
                    h[2],
                    h[3] if h[3] else '-',
                    estado,
                    h[5]
                )
            )
    def ver_detalle(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning('Aviso','Selecciona un equipo')
            return

        item = seleccionado[0]
        valores = self.tabla.item(item)['values']

        VentanaDetalleEquipo(self.root, valores)

