import tkinter as tk
from tkinter import messagebox

from ui.ventana_modelo import VentanaModelo
from ui.ventana_equipo import VentanaEquipo
from ui.ventana_cliente import VentanaCliente
from ui.ventana_asignacion import VentanaAsignacion
from ui.ventana_mantenimiento import VentanaMantenimiento
from ui.ventana_cliente_equipos import VentanaClienteEquipos
from ui.ventana_fallas_modelo import VentanaFallasModelo
from models.mantenimiento import Mantenimiento
from ui.ventana_usuarios import VentanaUsuario
from ui.dashboard import Dashboard
from ui.ventana_proveedores import VentanaProveedor

class VentanaPrincipal:

    def __init__(self, root, rol):

        self.root = tk.Toplevel(root)
        self.rol = str(rol).strip().upper()
        #print('ROL NORMALIZADO: ', self.rol)

        self.root.title('🧑‍💻 ≽^•⩊•^≼ Sistema inventario Tecnico by Lalito ≽^•⩊•^≼ 😎')
        self.root.geometry('600x500')


        self.root.after(1000, self.mostrar_alertas)

        titulo = tk.Label(
            self.root,
            text='🤘 Inventario Tecnico 🤘',
            font=('Arial',18)
        )
        titulo.pack(pady=20)

        btn_dashboard = tk.Button(
            self.root,
            text='📊 Dashboard',
            width=25,
            command=self.abrir_dashboard
        )

        btn_modelos = tk.Button(
            self.root,
            text='📀 Registro de Modelos',
            width=25,
            command=self.abrir_modelos
        )

        btn_clientes = tk.Button(
            self.root,
            text='👥 Registro de Clientes',
            width=25,
            command=self.abrir_clientes
        )

        btn_equipos = tk.Button(
            self.root,
            text='⚙️ Almacen 👨‍🔧',
            width=25,
            command=self.abrir_equipo
        )

        btn_asignacion = tk.Button(
            self.root,
            text='🏢 Asignacion de equipos  ',
            width=25,
            command=self.abrir_asignacion
        )

        btn_mantenimiento = tk.Button(
            self.root,
            text='📅 Tickets de Servicios  ',
            width=25,
            command=self.abrir_mantenimiento
        )

        btn_equipos_cliente = tk.Button(
            self.root,
            text='🤝 Consultas (Clientes) ',
            width=25,
            command=self.abrir_equipos_cliente
        )

        btn_fallas = tk.Button(
            self.root,
            text='📝 Guia de Fallas',
            width=25,
            command=self.abrir_fallas
        )

        btn_usuarios = tk.Button(
            self.root,
            text='👤 Usuarios',
            width=25,
            command=self.usuarios
        )

        btn_proveedor = tk.Button(
            self.root,
            text='📦 Proveedores',
            width=25,
            command=self.abrir_proveedor
        )

        if self.rol == 'ADMIN':
            btn_modelos.pack(pady=5)
            btn_clientes.pack(pady=5)
            btn_equipos.pack(pady=5)
            btn_asignacion.pack(pady=5)
            btn_usuarios.pack(pady=5)
            btn_proveedor.pack(pady=5)
            btn_equipos_cliente.pack(pady=5)
            btn_dashboard.pack(pady=5)
            btn_mantenimiento.pack(pady=5)
            btn_fallas.pack(pady=5)


    def abrir_modelos(self):

        VentanaModelo(self.root)

    def abrir_equipo(self):

        VentanaEquipo(self.root)

    def abrir_clientes(self):

        VentanaCliente(self.root)

    def abrir_asignacion(self):

        VentanaAsignacion(self.root)

    def abrir_mantenimiento(self):

        VentanaMantenimiento(self.root)

    def abrir_equipos_cliente(self):

        VentanaClienteEquipos(self.root)

    def abrir_fallas(self):
        VentanaFallasModelo(self.root)

    def usuarios(self):
        VentanaUsuario(self.root)

    def abrir_dashboard(self):
        Dashboard(self.root, self.rol)

    def abrir_proveedor(self):
        VentanaProveedor(self.root)

    def mostrar_alertas(self):

        alertas = Mantenimiento.proximos_mantenimientos()

        # print('alertas: ', alertas)

        if not alertas:
            return

        mensaje = 'Mantenimientos proximos: \n\n'

        for a in alertas:
            mensaje += f'* {a[1]} → {a[2]}\n'

        messagebox.showwarning('Alerta', mensaje)
