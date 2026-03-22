import tkinter as tk

from ui.ventana_modelo import VentanaModelo
from ui.ventana_equipo import VentanaEquipo
from ui.ventana_cliente import VentanaCliente
from ui.ventana_asignacion import VentanaAsignacion
from ui.ventana_mantenimiento import VentanaMantenimiento
from ui.ventana_cliente_equipos import VentanaClienteEquipos

class VentanaPrincipal:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title('🧑‍💻 ≽^•⩊•^≼ Sistema inventario Tecnico by Lalito ≽^•⩊•^≼ 😎')
        self.root.geometry('510x350')

        titulo = tk.Label(
            self.root,
            text='🤘 Inventario Tecnico 🤘',
            font=('Arial',18)
        )
        titulo.pack(pady=20)

        btn_modelos = tk.Button(
            self.root,
            text='📀 Registro de Modelos',
            width=20,
            command=self.abrir_modelos
        )
        btn_modelos.pack(pady=5)

        btn_clientes = tk.Button(
            self.root,
            text='👥 Registro de Clientes',
            width=20,
            command=self.abrir_clientes
        )
        btn_clientes.pack(pady=5)

        btn_equipos = tk.Button(
            self.root,
            text='⚙️ Equipo 👨‍🔧',
            width=20,
            command=self.abrir_equipo
        )
        btn_equipos.pack(pady=5)

        btn_asignacion = tk.Button(
            self.root,
            text='🏢 Asignaciones',
            width=20,
            command=self.abrir_asignacion
        )
        btn_asignacion.pack(pady=5)

        btn_mantenimiento = tk.Button(
            self.root,
            text='📅 Mantenimientos',
            width=20,
            command=self.abrir_mantenimiento
        )
        btn_mantenimiento.pack(pady=5)

        btn_equipos_cliente = tk.Button(
            self.root,
            text='🤝 Consultas',
            width=20,
            command=lambda: VentanaClienteEquipos(self.root)
        )
        btn_equipos_cliente.pack(pady=5)

        self.root.mainloop()

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