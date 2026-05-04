import time
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
from datetime import datetime, date
from tkcalendar import DateEntry
import os


from models.falla_modelo import FallaModelo
from models.mantenimiento import Mantenimiento
from models.equipo import Equipo
from utils.email_sender import enviar_correo
from models.usuario import Usuario
from utils.rutas import obtener_ruta_archivos
import shutil
from utils.exportar_excel import exportar_treeview

class VentanaMantenimiento:

    def __init__(self, parent):

        self.root = tk.Toplevel(parent)
        self.root.title('Mantenimiento')
        self.root.geometry('1600x800')
        self.root.update_idletasks()

        # Centrar ventanas
        ancho = 1600
        alto = 800

        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)

        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')

        # ===== EQUIPO =====
        tk.Label(self.root, text='Equipo').pack()

        self.equipos = Equipo.listar()

        equipo_text = [
            f'{e[1]} - {e[3]} {e[4]}'
            for e in self.equipos
        ]

        self.equipo_var = tk.StringVar()

        self.combo_equipo = ttk.Combobox(
            self.root,
            textvariable=self.equipo_var,
            values=equipo_text
        )

        self.combo_equipo.pack()
        self.combo_equipo.bind('<<ComboboxSelected>>', self.cargar_fallas_sugeridas)

        tk.Label(self.root, text='Fallas sugeridas').pack()

        self.lista_fallas = tk.Listbox(self.root, height=5)
        self.lista_fallas.pack(fill='x')

        # ===== TIPO =====
        tk.Label(self.root, text='Tipo').pack()

        self.tipo_var = tk.StringVar()

        self.combo_tipo =ttk.Combobox(
            self.root,
            textvariable=self.tipo_var,
            values=['PREVENTIVO', 'CORRECTIVO']
        )

        self.combo_tipo.pack()

        # ===== FECHA =====
        tk.Label(self.root, text='Fecha programada').pack()

        self.fecha = DateEntry(
            self.root,
            date_pattern='yyyy-mm-dd'
        )
        self.fecha.pack(pady=5)

        # ===== DESCRIPCION =====
        tk.Label(self.root, text='Descripcion').pack()

        self.descripcion = tk.Text(self.root, height=4, width=60)
        self.descripcion.pack(pady=5)

        # ===== TECNICO =====
        tk.Label(self.root, text='Tecnico').pack()

        self.tecnicos = Usuario.listar_tecnicos()

        nombres = [t[1] for t in self.tecnicos]

        self.tecnico_combo = ttk.Combobox(
            self.root,
            values=nombres,
            state='readonly'
        )
        self.tecnico_combo.pack()

        # ===== BOTON AGENDAR Y CERRAR MANTENIMIENTO =====
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones,
                  text="Agendar mantenimiento",
                  command=self.guardar_mantenimiento).pack(side="left", padx=5)
        tk.Button(frame_botones,
                  text="Cerrar mantenimiento agendado",
                  command=self.completar_mantenimiento).pack(side="left", padx=5)

        # Ingresar archivo de reporte
        tk.Button(frame_botones,
                  text='Adjuntar reporte de servicio',
                  command=self.adjuntar_reporte).pack(side="left", padx=5)
        tk.Button(frame_botones,
                  text='Abrir reportes',
                  command=self.abrir_reportes).pack(side="right", padx=5)

        # ===== Diagnostico ======
        tk.Button(frame_botones,
                  text='Diagnostico',
                  command=self.abrir_diagnostico).pack(side='right', padx=5)

        # ===== TABLA =====

        self.tabla = ttk.Treeview(
            self.root,
            columns=('ID', 'Equipo', 'Tipo', 'Fecha', 'Estado', 'Archivo'),
            show='headings',
        )

        self.tabla.heading('ID', text='ID')
        self.tabla.heading('Equipo', text='Equipo')
        self.tabla.heading('Tipo', text='Tipo')
        self.tabla.heading('Fecha', text='Fecha')
        self.tabla.heading('Estado', text='Estado')
        self.tabla.heading('Archivo', text='Archivo')
        self.tabla.tag_configure("PENDIENTE", background="#fff3cd")  # amarillo
        self.tabla.tag_configure("REALIZADO", background="#d4edda")  # verde
        self.tabla.pack(pady=20, fill='both', expand=True)

        self.cargar_mantenimientos()


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

    # ====================
    # GUARDAR
    # ====================

    def guardar_mantenimiento(self):

        equipo_index = self.combo_equipo.current()

        if equipo_index == -1:
            messagebox.showwarning('Aviso', 'Selecciona un equipo')
            return

        id_equipo = self.equipos[equipo_index][0]

        tipo = self.tipo_var.get()
        if not tipo:
            messagebox.showwarning('Aviso',
                                   'Selecciona el tipo de mantenimiento')
            return

        fecha = self.fecha.get_date()

        try:
            if isinstance(fecha, str):
                fecha_dt = datetime.strptime(fecha, '%Y-%m-%d').date()
            else:
                fecha_dt = fecha
                if fecha_dt.year < 2000 or fecha_dt.year > 2100:
                    messagebox.showerror(
                        "Error",
                        "Fecha fuera de rango válido"
                    )
                    return
        except ValueError:
            messagebox.showwarning('Aviso',
                                   'la fecha debe tener formato YYYY-MM-DD')
            return

        descripcion = self.descripcion.get('1.0', tk.END).strip()

        index = self.tecnico_combo.current()

        if index == -1:
            messagebox.showwarning('Aviso', 'Selecciona un tecnico')
            return

        tecnico = self.tecnicos[index][1]

        mantenimiento = Mantenimiento(
            id_equipo,
            tipo,
            fecha,
            descripcion,
            tecnico
        )

        mantenimiento.guardar()

        emails = Usuario.obtener_email()
        mensaje = f'''
        Nuevo mantenimiento asignado.

        ID de quipo: {id_equipo}
        Tipo: {tipo}
        Fecha de servicio:{fecha}
        Tecnico: {tecnico}
        Descripcion de servicio: {descripcion}
        '''

        enviar_correo(emails,
                      'Nuevo mantenimiento asignado',
                      mensaje
                      )

        messagebox.showinfo('Exito', 'Mantenimiento registrado')

        self.cargar_mantenimientos()

    # ==========================
    # LISTAR
    # ==========================

    def cargar_mantenimientos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        mantenimientos = Mantenimiento.listar()

        for m in mantenimientos:

            equipo_texto = f'{m[1] or 'SIN SERIE'} - {m[2]} {m[3]}'
            tiene_archivo = '📎' if m[8] or m[9] else ''

            self.tabla.insert(
                '',
                'end',
                values=(
                    m[0], # id
                    equipo_texto, # Equipo
                    m[4], # tipo
                    m[5], # fecha_programada
                    m[7],
                    tiene_archivo# estado
                ),
                tags=(m[7])
            )

    # =========================
    # COMPLETAR
    # =========================

    def completar_mantenimiento(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning('Aviso', 'Selecciona un mantenimiento')
            return

        item = seleccionado[0]
        valores = self.tabla.item(item)['values']

        id_mantenimiento = valores[0]
        estado_actual = valores[4] # Columna estado

        # Validar si ya esta realizado
        if estado_actual == 'REALIZADO':
            messagebox.showwarning(
                'Aviso',
                'Este mantenimiento ya esta realizado'
            )
            return

        # Pedir una solucion Obligatoria
        solucion = simpledialog.askstring(
            'Resolucion',
            'Describe la solucion aplicada: '
        )

        if not solucion:
            messagebox.showwarning('Aviso', 'Debes ingresar la solucion')
            return

        # Guardar
        Mantenimiento.completar(id_mantenimiento, solucion)

        emails = Usuario.obtener_email()

        mensaje = f'''
        Mantenimiento Finalizado
        ID de mantenimiento: {id_mantenimiento}
        solucion: {solucion}
        Fecha: {datetime.now().date()}
        '''
        enviar_correo(
            emails,
            'Servicio completado',
            mensaje
        )

        self.cargar_mantenimientos()

        messagebox.showinfo('Exito', 'Mantenimiento completado')

    def cargar_fallas_sugeridas(self, event=None):

        self.lista_fallas.delete(0, tk.END)

        equipo_index = self.combo_equipo.current()

        if equipo_index == -1:
            return

        # Id modelo
        id_modelo = self.equipos[equipo_index][6]

        fallas = FallaModelo.listar_por_modelo(id_modelo)

        for f in fallas:
            texto = f'{f[0]} - {f[1]}'
            self.lista_fallas.insert(tk.END, texto)

    def obtener_mantenimiento_seleccionado(self):

        selected = self.tabla.selection()

        if not selected:
            messagebox.showwarning('Aviso', 'Selecciona un mantenimiento para adjuntar archivo')
            return None

        valores = self.tabla.item(selected[0])['values']

        return valores

    def adjuntar_reporte(self):

        mantenimiento = self.obtener_mantenimiento_seleccionado()

        if not mantenimiento:
            return

        id_mantenimiento = mantenimiento[0]
        estado = mantenimiento[4]

        if estado != 'REALIZADO':
            messagebox.showwarning(
                'Aviso',
                'Solo puedes adjuntar reporte a mantenimientos COMPLETADOS'
            )
            return

        ruta_original = filedialog.askopenfilename(
            title='Seleccionar reporte',
            filetypes=[
                ('PDF', '*.pdf'),
                ('Word', '*.docx'),
                ('Todos', '*.*')
            ]
        )

        if not ruta_original:
            return

        ruta_base = obtener_ruta_archivos('Mantenimientos')

        nombre = f'{id_mantenimiento}_Mantenimiento_{int(time.time())}.pdf'

        ruta_destino = os.path.join(ruta_base, nombre)
        try:
            shutil.copyfile(ruta_original, ruta_destino)
        except Exception as e:
            messagebox.showerror('Aviso', f'No se pudo guardar archivo:\n{e}')
            return

        Mantenimiento.guardar_reporte(id_mantenimiento, ruta_destino)
        # print('Guardado en: ', ruta_destino)

        messagebox.showinfo('Exito', 'Reporte adjuntado correctamente')

    def abrir_reportes(self):

        mantenimiento = self.obtener_mantenimiento_seleccionado()

        if not mantenimiento:
            messagebox.showwarning('Aviso', 'Selecciona un mantenimiento')
            return

        id_mantenimiento = mantenimiento[0]

        ruta_diag = Mantenimiento.obtener_archivo_diagnostico(id_mantenimiento)
        ruta_rep = Mantenimiento.obtener_reporte(id_mantenimiento)

        opciones = []

        if ruta_diag:
            opciones.append('Diagnostico')

        if ruta_rep:
            opciones.append('Reporte')

        if not opciones:
            messagebox.showwarning('Aviso', 'No hay archivos disponibles')
            return

        # Si solo hay una -> abrir directo
        if len(opciones) == 1:
            self.abrir_archivo(opciones[0], ruta_diag, ruta_rep)

        # Si hay dos -> elegir
        self.mostrar_opciones_archivo(opciones, ruta_diag, ruta_rep)

    def mostrar_opciones_archivo(self, opciones, ruta_diag, ruta_rep):

        ventana =tk.Toplevel(self.root)
        ventana.title('Abrir archivo')
        ancho = 350
        alto = 200

        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)

        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
        ventana.transient(self.root)
        ventana.grab_set()


        tk.Label(ventana, text='Selecciona que archivo abrir: ').pack(pady=10)

        if 'Diagnostico' in opciones:
            tk.Button(
                ventana,
                text='Abrir Diagnostico',
                command=lambda: self.ejecutar_apertura(ruta_diag, ventana)
            ).pack(pady=5)

        if 'Reporte' in opciones:
            tk.Button(
                ventana,
                text='Abrir Reporte',
                command=lambda: self.ejecutar_apertura(ruta_rep, ventana)
            ).pack(pady=5)

    def ejecutar_apertura(self, ruta, ventana):

        if ruta and os.path.exists(ruta):
            os.startfile(ruta)
            ventana.destroy()
        else:
            messagebox.showwarning('Aviso', 'Archivo no encontrado')

    def abrir_archivo(self, tipo, ruta_diag, ruta_rep):

        ruta = ruta_diag if tipo == 'Diagnostico' else ruta_rep

        if ruta and os.path.exists(ruta):
            os.startfile(ruta)
        else:
            messagebox.showwarning('Aviso', 'Archivo no encontrado')

    def abrir_diagnostico(self):

        mantenimiento = self.obtener_mantenimiento_seleccionado()

        if not mantenimiento:
            return

        id_mantenimiento = mantenimiento[0]

        ventana = tk.Toplevel(self.root)
        ventana.title('Diagnostico')

        tk.Label(ventana, text='Diagnostico').pack()

        texto = tk.Text(ventana, height=10, width=50)
        texto.pack()

        tk.Button(ventana, text='Correctivo', command=lambda: cambiar_tipo('CORRECTIVO')).pack()
        tk.Button(ventana, text='Preventivo', command=lambda: cambiar_tipo('PREVENTIVO')).pack()

        def cambiar_tipo(nuevo_tipo):

            Mantenimiento.actualizar_tipo(id_mantenimiento, nuevo_tipo)
            messagebox.showinfo('Exito', f"Cambiado a {nuevo_tipo}")
            self.cargar_mantenimientos()

        def adjuntar_archivo_diag():
            from utils.rutas import obtener_ruta_archivos
            import shutil
            import os

            ruta_original = filedialog.askopenfilename(
                title='Seleccionar archivo de diagnostico',
                filetypes=[
                    ('PDF', '*.pdf'),
                    ('Word', '*.docx'),
                    ('Todos', '*.*')
                ]
            )

            if not ruta_original:
                return

            ruta_base = obtener_ruta_archivos('Diagnosticos')

            nombre = f'{id_mantenimiento}_Diagnostico_{int(time.time())}.pdf'

            ruta_destino = os.path.join(ruta_base, nombre)

            try:
                shutil.copyfile(ruta_original, ruta_destino)
            except Exception as e:
                messagebox.showerror('Error', f'No se pudo guardar archivo:\n{e}')
                return

            Mantenimiento.guardar_archivo_diagnostico(id_mantenimiento, ruta_destino)

            messagebox.showinfo('Exito', "Archivo de diagnostico guardado")

        tk.Button(
            ventana,
            text='Adjuntar archivo diagnostico',
            command=adjuntar_archivo_diag
        ).pack()

        def guardar():
            diagnostico = texto.get('1.0', tk.END).strip()

            if not diagnostico:
                messagebox.showwarning('Aviso', 'Introduce un diagnostico')
                return

            Mantenimiento.guardar_diagnostico(id_mantenimiento, diagnostico)

            messagebox.showinfo('Exito', "Diagnostico guardado")
            ventana.destroy()

        tk.Button(ventana, text='Guardar estado', command=guardar).pack()
