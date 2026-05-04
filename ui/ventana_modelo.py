import tkinter as tk
from tkinter import messagebox

from models.modelo import Modelo


class VentanaModelo:

    def __init__(self, parent):

        self.root = tk.Toplevel(parent)
        self.root.title('Registro de Modelos')
        self.root.geometry('400x250')

        # Marca fabricante
        tk.Label(self.root, text='Marca Fabricante').pack()
        self.marca_fabricante = tk.Entry(self.root, width=35)
        self.marca_fabricante.pack()

        # Modelo fabricante
        tk.Label(self.root, text="Modelo Fabricante").pack()
        self.modelo_fabricante = tk.Entry(self.root, width=35)
        self.modelo_fabricante.pack()

        # Marca comercial
        tk.Label(self.root, text='Marca Comercial').pack()
        self.marca_comercial = tk.Entry(self.root, width=35)
        self.marca_comercial.pack()

        # Modelo comercial
        tk.Label(self.root, text='Modelo Comercial').pack()
        self.modelo_comercial = tk.Entry(self.root, width=35)
        self.modelo_comercial.pack()

        # Descripcion
        tk.Label(self.root, text='Descripcion', width=35).pack()
        self.descripcion = tk.Entry(self.root)
        self.descripcion.pack(fill='x', padx=10)

        # Boton guardar
        tk.Button(
            self.root,
            text='Guardar Modelo',
            command=self.guardar_modelo
        ).pack(pady=10)

        self.root.mainloop()

    def guardar_modelo(self):

        marca_fab = self.marca_fabricante.get().strip()
        modelo_fab = self.modelo_fabricante.get().strip()
        marca_com = self.marca_comercial.get().strip()
        modelo_com = self.modelo_comercial.get().strip()
        descripcion = self.descripcion.get().strip()

        if not all([marca_fab, modelo_fab, marca_com, modelo_com, descripcion]):
            messagebox.showerror(
                "Aviso",
                "No puedes dejar campos en blanco"
            )
            return

        if len(modelo_fab) < 2:
            messagebox.showerror(
                'Aviso',
                'Modelo fabricante muy corto'
            )
        if len(marca_com) < 2:
            messagebox.showerror(
                'Aviso',
                'Modelo comercial muy corto'
            )

        modelo = Modelo(
            marca_fab,
            modelo_fab,
            marca_com,
            modelo_com,
            descripcion
        )

        modelo.guardar()

        messagebox.showinfo('Exito', 'Modelo guardado')

        self.marca_fabricante.delete(0, tk.END)
        self.modelo_fabricante.delete(0, tk.END)
        self.marca_comercial.delete(0, tk.END)
        self.modelo_comercial.delete(0, tk.END)
        self.descripcion.delete(0, tk.END)

