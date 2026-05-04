import tkinter as tk
from tkinter import messagebox

class Mainapp:

    def __init__(self, root, rol):

        self.root = root
        self.rol = rol

        self.root.title('Sistema')
        self.root.geometry('600x300')

        #Colores
        color_fondo = "#F3F4F6"
        color_texto = "#111827"
        color_texto2 = "#6366F1"

        tk.Label(root,
                 fg="Blue",
                 font=("Segoe UI", 11, "bold"),
                 text=f'User role: {rol}'
                 ).pack(pady=10)

        # Botones segun rol

        if self.rol == 'ADMIN':
            tk.Button(root, text='⚙️ Equipos 👨‍🔧',
                      bg=color_fondo,
                      fg=color_texto,
                      command=self.abrir_equipos,
                      width=25
                      ).pack(pady=5)

        tk.Button(root,
                  text='Dashboard',
                  bg=color_fondo,
                  fg=color_texto2,
                  command=self.abrir_dashboard,
                  width=25
                  ).pack(pady=5)
        tk.Button(root,
                  text='Equipos cliente',
                  bg=color_fondo,
                  fg=color_texto2,
                  command=self.abrir_equipos_cliente,
                  width=25
                  ).pack(pady=5)
        tk.Button(root,
                  text='Mantenimientos',
                  bg=color_fondo,
                  fg=color_texto2,
                  command=self.abrir_mantenimientos,
                  width=25
                  ).pack(pady=5)
        tk.Button(root,
                  text='📝 Fallas',
                  bg=color_fondo,
                  fg=color_texto2,
                  command=self.abrir_fallas,
                  width=25
                  ).pack(pady=5)


        tk.Button(
            self.root,
            text='🔒 Cerrar sesión',
            width=25,
            fg="red",
            font=("Segoe UI", 11, "bold"),
            command=self.cerrar_sesion
        ).pack(pady=10)

    def abrir_equipos(self):
        from ui.ventana_principal import VentanaPrincipal
        VentanaPrincipal(self.root, self.rol)

    def abrir_equipos_cliente(self):
        from ui.ventana_cliente_equipos import VentanaClienteEquipos
        VentanaClienteEquipos(self.root)


    def abrir_mantenimientos(self):
        from ui.ventana_mantenimiento import VentanaMantenimiento
        VentanaMantenimiento(self.root)

    def abrir_fallas(self):
        from ui.ventana_fallas_modelo import VentanaFallasModelo
        VentanaFallasModelo(self.root)

    def abrir_dashboard(self):
        from ui.ventana_principal import Dashboard
        Dashboard(self.root, self.rol)

    def eliminar_mantenimiento(self):

        if self.rol != 'ADMIN':
            messagebox.showerror('Acceso denegado', "No tienes privilegios")
            return

    def cerrar_sesion(self):

        self.root.destroy()

        import tkinter as tk
        from ui.login import VentanaLogin

        root = tk.Tk()
        VentanaLogin(root)
        root.mainloop()