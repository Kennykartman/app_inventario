import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry

from models.mantenimiento import Mantenimiento
from models.equipo import Equipo

class VentanaMantenimiento:

    def __init__(self, parent):

        self.root = tk.Toplevel(parent)
        self.root.title('Mantenimiento')
        self.root.geometry('1000x600')

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

        self.tecnico = tk.Entry(self.root)
        self.tecnico.pack()

        # ===== BOTON AGENDAR Y CERRAR MANTENIMIENTO =====
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones,
                  text="Agendar mantenimiento",
                  command=self.guardar_mantenimiento).pack(side="left", padx=5)
        tk.Button(frame_botones,
                  text="Cerrar mantenimiento agendado",
                  command=self.completar_mantenimiento).pack(side="left", padx=5)

        # ===== TABLA =====
        self.tabla = ttk.Treeview(
            self.root,
            columns=('ID', 'Equipo', 'Tipo', 'Fecha', 'Estado'),
            show='headings',
        )

        self.tabla.heading('ID', text='ID')
        self.tabla.heading('Equipo', text='Equipo')
        self.tabla.heading('Tipo', text='Tipo')
        self.tabla.heading('Fecha', text='Fecha')
        self.tabla.heading('Estado', text='Estado')
        self.tabla.tag_configure("PENDIENTE", background="#fff3cd")  # amarillo
        self.tabla.tag_configure("REALIZADO", background="#d4edda")  # verde

        self.tabla.pack(pady=20, fill='both', expand=True)

        self.cargar_mantenimientos()



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
        fecha = self.fecha.get()
        try:
            fecha_dt = datetime.strptime(fecha, '%Y-%m-%d')
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
        tecnico = self.tecnico.get()

        mantenimiento = Mantenimiento(
            id_equipo,
            tipo,
            fecha,
            descripcion,
            tecnico
        )

        mantenimiento.guardar()

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

            self.tabla.insert(
                '',
                'end',
                values=(
                    m[0], # id
                    m[1], # Equipo
                    m[2], # tipo
                    m[3], # fecha_programada
                    m[5] # estado
                ),
                tags=(m[5])
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

        Mantenimiento.completar(id_mantenimiento)

        self.cargar_mantenimientos()

        messagebox.showinfo('Exito', 'Mantenimiento completado')
