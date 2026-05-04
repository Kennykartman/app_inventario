import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from psycopg2 import errors
from datetime import datetime

from models.asignacion import Asignacion
from models.equipo import Equipo
from models.modelo import Modelo
from ui.ventana_detalle_equipo import VentanaDetalleEquipo
from utils.exportar_excel import exportar_treeview



class VentanaEquipo:

    def __init__(self, parent):

        self.root = tk.Toplevel(parent)
        self.root.title("Equipos de almacen")
        self.root.geometry("1100x750")
        self.centrar_ventana()
        self.root.update_idletasks()


        tk.Label(self.root, text="📦 Registro de equipos nuevos", font=("Arial", 12, "bold")).pack()

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
            values=modelos_text,
            width=35
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

        # Busqueda
        tk.Label(self.root, text='Buscar equipo').pack()

        self.busqueda = tk.Entry(self.root)
        self.busqueda.pack()

        self.busqueda.bind('<KeyRelease>', self.buscar_equipo)

        # Ventana de equipos
        tk.Label(
            self.root,
            text='Equipos registrados en almacen',
            font=('Arial',12,'bold')
        ).pack(pady=10)

        self.tabla = ttk.Treeview(
            self.root,
            columns=('ID', "Serie", 'Marca', "Modelo", "Estado", 'Tipo', 'Garantia', 'Dias'),
            show="headings"
        )

        self.tabla.pack(fill='both', expand=True)

        self.tabla.heading('ID', text='ID')
        self.tabla.heading("Serie", text="Serie Interna")
        self.tabla.heading("Marca", text="Marca")
        self.tabla.heading("Modelo", text="Modelo")
        self.tabla.heading("Estado", text="Estado")
        self.tabla.heading('Tipo', text="Asignacion")
        self.tabla.heading('Garantia', text=" Fin de garantia")
        self.tabla.heading('Dias', text="Dias restantes")
        self.tabla.column("ID", width=50, anchor='center')
        self.tabla.column("Serie", width=120)
        self.tabla.column("Marca", width=120)
        self.tabla.column("Modelo", width=150)
        self.tabla.column("Estado", width=100)
        self.tabla.column("Tipo", width=120)
        self.tabla.column("Garantia", width=130)
        self.tabla.column("Dias", width=120)
        self.tabla.tag_configure('ALMACEN', background='#d0e7ff')
        self.tabla.tag_configure('INSTALADO', background='#d4f7d4')
        self.tabla.tag_configure('REPARACION', background='#fff3dc')
        self.tabla.tag_configure('BAJA', background='#f8d7da')


        scroll_y = ttk.Scrollbar(self.root, orient="vertical", command=self.tabla.yview)
        scroll_y.pack(side="right", fill="y")

        self.tabla.configure(yscrollcommand=scroll_y.set)

        # cargar datos
        self.cargar_equipos()

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)


        tk.Button(frame_botones,
                  text='Instalar',
                  command=lambda: self.cambiar_estado('INSTALADO'),
                  width=20
                  ).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(frame_botones,
                  text='Reparacion',
                  command=lambda: self.cambiar_estado('REPARACION'),
                  width=20).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(frame_botones,
                  text='Dar de baja',
                  command=lambda: self.cambiar_estado('BAJA'),
                  width=20).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(frame_botones,
                  text='Regresar a almacen',
                  command=lambda: self.cambiar_estado('ALMACEN'),
                  width=20).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(frame_botones,
                  text='Ver historia',
                  command=lambda: self.ver_historial(),
                  width=20).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(frame_botones,
                  text='Ver Detalle',
                  command=lambda: self.ver_detalle(),
                  width=20).grid(row=2, column=1, padx=5, pady=5)

        tk.Button(frame_botones,
                  text='📥 Exportar TODO',
                  command=lambda: exportar_treeview(self.tabla),
                  width=20).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(frame_botones,
                  text='🗃️ Exportar Seleccionado',
                  command=lambda: exportar_treeview(self.tabla, True),
                  width=20).grid(row=3, column=1, padx=5, pady=5)

    def cambiar_estado(self, nuevo_estado):

        equipo = self.obtener_equipo_seleccionado()

        if not equipo:
            messagebox.showwarning(
                'Aviso',
                'Selecciona un equipo primero'
            )
            return

        id_equipo = equipo[0]
        estado_actual = equipo[4]

        # Bloqueo: Si esta dado de baja -> no permite cambios
        if estado_actual == 'BAJA':
            messagebox.showerror(
                'Error',
                'Este equipo esta dado de baja y NO puede modificarse'
            )
            return

        # Si quiere darse de baja
        if nuevo_estado == 'BAJA':

            motivo = simpledialog.askstring(
                'Motivo de la baja',
                'Ingrese el motivo de la baja: '
            )

            if not motivo:
                messagebox.showwarning('Aviso','Debes de ingresar un motivo')
                return

            confirmacion = messagebox.askyesno(
                'Confirmacion de baja',
                'Seguro que desea dar de baja el equipo?\n\nEsta accion no puede revertirse: '
            )

            if not confirmacion:
                return

            #Actualizar
            Equipo.dar_de_baja(id_equipo, motivo)

            messagebox.showinfo('Exito', 'Equipo dado de baja correctamente')

        else:
            #Cambio normal
            Equipo.actualizar_estado(id_equipo, nuevo_estado)

            messagebox.showinfo(
                'Exito',
                f'Estado cambiado a {nuevo_estado}'
            )

        self.cargar_equipos()

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
            tipo = e[8] if e[8] else 'TEMPORAL'
            fecha_fin = e[9]
            dias = self.calcular_dias_restantes(fecha_fin)

            self.tabla.insert(
                "",
                "end",
                values=(
                    e[0],      # id_equipo
                    e[1],      # serie interna
                    marca,     # modelo interno
                    modelo,    # modelo
                    estado,     # estado
                    tipo,
                    fecha_fin if fecha_fin else '-',
                    dias
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

    def calcular_dias_restantes(self, fecha_fin):

        if not fecha_fin:
            return '-'

        hoy = datetime.now().date()
        dias = (fecha_fin-hoy).days

        return dias

    def centrar_ventana(self):

        self.root.update_idletasks()

        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()

        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)

        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")

