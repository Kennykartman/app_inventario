import tkinter as tk

from models.mantenimiento import Mantenimiento
from models.equipo import Equipo

class Dashboard:

    def __init__(self, root, rol):

        self.root = tk.Toplevel(root)
        self.rol = rol
        self.root.title("📊 Dashboard")

        ancho = 1000
        alto = 700

        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)

        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')
        self.root.transient(root)
        self.root.grab_set()

        tk.Label(
            self.root,
            text="📊 Dashboard",
            font=("Segoe UI", 20)
        ).pack(pady=10)

        self.frame = tk.Frame(self.root, bg='#f5f6fa')
        self.frame.pack(fill='both', expand=True, padx=20, pady=20)
        self.cards_frame = tk.Frame(self.frame, bg='#f5f6fa')
        self.cards_frame.pack(fill='x', pady=10)

        for i in range(4):
            self.cards_frame.grid_columnconfigure(i, weight=1)

        self.bottom_frame = tk.Frame(self.frame, bg='#f5f6fa')
        self.bottom_frame.pack(fill='both', expand=True, pady=10)
        self.bottom_frame.grid_rowconfigure(0, weight=1)
        self.bottom_frame.grid_rowconfigure(1, weight=1)

        self.cargar_datos()

    def cargar_datos(self):

        # Mantenimiento proximos
        mantenimientos = Mantenimiento.proximos_mantenimientos()
        total_mantenimientos = len(mantenimientos)

        # Equipos activos
        equipos = Equipo.listar()
        total_equipos = len(equipos)

        # Total de pendientes
        mantenimientos_pend = Mantenimiento.contar_pendientes()
        vencidos = Mantenimiento.contar_vencidos()
        por_tecnico = Mantenimiento.mantenimientos_por_tecnico()

        # Tarjetas
        self.crear_tarjeta(
            '⏲️ Servicios proximos',
            total_mantenimientos,'#696969',
            0,
            'Proximos dias'
        )

        self.crear_tarjeta(
            '💻 Equipos totales',
            total_equipos,
            '#2ecc71',
            1,
            'Activos en sistema'
        )

        self.crear_tarjeta(
            '🛠️ Total de pendientes',
            mantenimientos_pend,
            '#3498db',
            2,
            'Requiere atencion'
        )

        self.crear_tarjeta(
            '🚨 Vencidos',
            vencidos,
            '#e74c3c',
            3,
            'Urgente'
        )


        frame_tecnico = tk.Frame(self.bottom_frame, bg='white')
        frame_tecnico.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        frame_alertas = tk.Frame(self.bottom_frame, bg='white')
        frame_alertas.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        tk.Label(
            frame_tecnico,
            text='🧑‍🔧 Mantenimiento por Tecnico',
            font=('Segoe UI', 15, 'bold')
        ).pack(pady=10)

        tk.Label(
            frame_alertas,
            text='⚠ Resumen',
            font=('Segoe UI', 12, 'bold'),
            bg='white'
        ).pack(pady=10)

        tk.Label(frame_alertas, text=f'Pendientes:      {mantenimientos_pend}', bg='white').pack(anchor='w', padx=10)
        tk.Label(frame_alertas, text=f'Vencidos:         {vencidos}', bg='white').pack(anchor='w', padx=10)
        tk.Label(frame_alertas, text=f'Próximos:         {total_mantenimientos}', bg='white').pack(anchor='w', padx=10)

        for t in por_tecnico:
            nombre = t[0] or 'Sin asignar'
            total = t[1]

            if total == 0:
                color = '#bdc3c7'  # gris
            elif total <= 2:
                color = '#2ecc71'  # verde
            elif total <= 4:
                color = '#f1c40f'  # amarillo
            else:
                color = '#e74c3c'  # rojo

            fila = tk.Frame(frame_tecnico, bg='white')
            fila.pack(fill='x', padx=10, pady=2)

            tk.Label(
                fila,
                text=nombre,
                bg='white',
                anchor='w'
            ).pack(side='left')

            tk.Label(
                fila,
                text=str(total),
                bg=color,
                fg='white',
                width=4
            ).pack(side='right')


    def crear_tarjeta(self, titulo, valor, color, columna, subtitulo=''):

        card = tk.Frame(
            self.cards_frame,
            bg=color,
            bd=0,
            relief='flat',
            height=120,
        )

        card.grid(row=0, column=columna, padx=10, pady=10, sticky='nsew')
        card.grid_propagate(False)

        tk.Label(
            card,
            text=titulo,
            bg=color,
            fg='white',
            font=('Segoe UI', 16)
        ).pack(pady=(8,2))

        tk.Label(
            card,
            text=str(valor),
            bg=color,
            fg='white',
            font=('Arial', 20, 'bold')
        ).pack(pady=(0, 2))

        tk.Label(
            card,
            text=subtitulo,
            bg=color,
            fg='#ecf0f1',
            font=('Segoe UI', 19, 'bold'),
            wraplength=120,
            justify='center'
        ).pack(pady=(0, 6))