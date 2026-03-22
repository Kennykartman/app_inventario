import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from models.cliente import Cliente


class VentanaCliente:

    def __init__(self, parent):

        self.root = tk.Toplevel(parent)
        self.root.title('Registro de Cliente')
        self.root.geometry('1300x600')

        # Nombre
        tk.Label(self.root, text='Nombre').pack()
        self.nombre = tk.Entry(self.root)
        self.nombre.pack()

        # Direccion
        tk.Label(self.root, text='Direccion').pack()
        self.direccion = tk.Entry(self.root)
        self.direccion.pack()

        # Telefono
        tk.Label(self.root, text='Telefono').pack()
        self.telefono = tk.Entry(self.root)
        self.telefono.pack()

        # email
        tk.Label(self.root, text='Email').pack()
        self.email = tk.Entry(self.root)
        self.email.pack()

        # contrato
        tk.Label(self.root, text='No. Contrato').pack()
        self.contrato = tk.Entry(self.root)
        self.contrato.pack()

        # boton guardar
        tk.Button(
            self.root,
            text='Guardar',
            command=self.guardar_cliente
        ).pack(pady=10)

        # tabla
        self.tabla = ttk.Treeview(
            self.root,
            columns=('ID', 'Nombre', 'Direccion', 'Telefono', 'Email', 'no_contrato'),
            show='headings',
        )

        self.tabla.heading('ID', text='ID')
        self.tabla.heading('Nombre', text='Nombre')
        self.tabla.heading('Direccion', text='Direccion')
        self.tabla.heading('Telefono', text='Telefono')
        self.tabla.heading('Email', text='Email')
        self.tabla.heading('no_contrato', text='No contrato')

        self.tabla.pack(pady=20, fill='both', expand=True)

        self.cargar_clientes()

    def cargar_clientes(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        cliente = Cliente.listar()

        for c in cliente:

            self.tabla.insert(
                '',
                'end',
                values=c
            )

    def guardar_cliente(self):

        nombre = self.nombre.get()
        direccion = self.direccion.get()
        telefono = self.telefono.get()
        email = self.email.get()
        no_contrato = self.contrato.get()

        if not nombre:
            messagebox.showwarning(
                'Aviso',
                'El nombre es obligatorio'
            )
            return

        if not no_contrato:
            messagebox.showwarning(
                'Aviso',
                'Debe ingresar numero de contrato'
            )
            return

        cliente = Cliente(
            nombre,
            direccion,
            telefono,
            email,
            no_contrato
        )

        cliente.guardar()

        messagebox.showinfo(
            'Exito',
            'Cliente registrado exitosamente'
        )

        self.cargar_clientes()

        self.nombre.delete(0, tk.END)
        self.direccion.delete(0, tk.END)
        self.telefono.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.contrato.delete(0, tk.END)
