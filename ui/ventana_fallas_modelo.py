import tkinter as tk
from tkinter import ttk, messagebox

from models.modelo import Modelo
from models.falla_modelo import FallaModelo


class VentanaFallasModelo:

    def __init__(self, parent):

        self.root = tk.Toplevel(parent)
        self.root.title('Fallas por modelo')
        self.root.geometry('800x600')


        # ===== Modelo =====
        tk.Label(self.root, text='Modelo').pack()
        self.modelos = Modelo.listar()
        modelos_text = [
            f'{m[1]} - {m[2]}' for m in self.modelos
        ]
        self.modelo_var = tk.StringVar()
        self.combo_modelo = ttk.Combobox(
            self.root,
            textvariable=self.modelo_var,
            values=modelos_text,
            width=35,
        )
        self.combo_modelo.pack()
        self.combo_modelo.bind('<<ComboboxSelected>>', self.cargar_fallas)

        # ===== CODIGO =====
        tk.Label(self.root, text='Codigo de falla (Opcional)').pack()

        self.codigo_entry = tk.Entry(self.root)
        self.codigo_entry.pack()

        # ===== Descripcion =====
        tk.Label(self.root, text='Descripcion de la falla').pack()

        self.descripcion = tk.Text(self.root, height=4)
        self.descripcion.pack()

        # ===== SOLUCION =====
        tk.Label(self.root, text='Solucion').pack()

        self.solucion = tk.Text(self.root, height=4)
        self.solucion.pack()

        # ===== BOTON =====
        tk.Button(
            self.root,
            text='Guardar falla',
            command=self.guardar_falla
        ).pack(pady=10)

        # ===== TABLA =====
        self.tabla = ttk.Treeview(
            self.root,
            columns=('codigo', 'descripcion', 'solucion'),
            show='headings'
        )

        self.tabla.heading('codigo', text='Codigo')
        self.tabla.heading('descripcion', text='Falla')
        self.tabla.heading('solucion', text='Solucion')

        self.tabla.pack(fill='both', expand=True)

        # ==================
        # GUARDAR
        # ==================

    def guardar_falla(self):

        modelo_index = self.combo_modelo.current()

        if modelo_index == -1:
            messagebox.showwarning('Aviso', 'Selecciona una modelo')
            return

        id_modelo = self.modelos[modelo_index][0]

        codigo = self.codigo_entry.get().strip()
        if not codigo:
            codigo = 'N/A'

        descripcion = self.descripcion.get('1.0', tk.END).strip()
        solucion = self.solucion.get('1.0', tk.END).strip()

        if not descripcion:
            messagebox.showwarning('Aviso', 'La descripcion es obligatoria')
            return

        falla = FallaModelo(
            id_modelo,
            descripcion,
            solucion,
            codigo
            )

        falla.guardar()

        messagebox.showinfo('Exito', 'Falla registrada')

        self.cargar_fallas()

        # Limpiar
        self.codigo_entry.delete(0, tk.END)
        self.descripcion.delete('1.0', tk.END)
        self.solucion.delete('1.0', tk.END)

        # ======================
        # LISTAR
        # ======================

    def cargar_fallas(self, event=None):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        modelo_index = self.combo_modelo.current()

        if modelo_index == -1:
            return

        id_modelo = self.modelos[modelo_index][0]

        fallas = FallaModelo.listar_por_modelo(id_modelo)

        for f in fallas:
            self.tabla.insert('', 'end', values=f)
