import sys
import os
import tkinter as tk

from PIL import Image, ImageTk

from models.usuario import Usuario
from utils.security import validar_password




class VentanaLogin:

    def __init__(self, root):

        self.root = root
        self.root.title("Humanet Cover")
        self.root.geometry('500x400')

        # Cargar logo
        def recurso_path(rel_path):
            if getattr(sys, 'frozen', False):
                base = sys._MEIPASS
            else:
                base = os.path.abspath('.')

            return os.path.join(base, rel_path)

        ruta_logo = recurso_path('assets/logo.png')


        img = Image.open(ruta_logo)
        img = img.resize((120, 120))

        self.logo = ImageTk.PhotoImage(img)

        label_logo = tk.Label(self.root, image=self.logo)
        label_logo.pack(pady=10)


        tk.Label(root, text="Usuario").pack(pady=5)
        self.usuario = tk.Entry(root)
        self.usuario.pack()

        tk.Label(root, text='Contraseña').pack(pady=5)
        self.password = tk.Entry(root, show='*')
        self.password.pack()

        tk.Button(
            root,
            text='Ingresar',
            command=self.login
        ).pack(pady=10)

        tk.Button(
            root,
            text='Configurar servidor',
            command=self.abrir_config
        ).pack()

    def login(self):

        user = self.usuario.get()
        pwd = self.password.get()

        try:
            from tkinter import messagebox
            import tkinter as tk

            resultado = Usuario.validar(user,pwd)

            if not resultado:
                messagebox.showerror("Error", "Credenciales incorrectas")
                return

            if resultado[4]: # Primer_login

                messagebox.showwarning(
                    "Cambio requerido",
                    "Debes cambiar tu contraseña",
                parent=self.root
                )

                from tkinter import simpledialog

                while True:

                    nueva = simpledialog.askstring(
                        'Cambio obligatorio',
                        'Nueva contraseña',
                        show='*',
                        parent=self.root
                    )

                    if not nueva:
                        continue

                    valido, msg = validar_password(nueva)

                    if not valido:
                        messagebox.showerror("Error", msg, parent=self.root)
                        continue

                    confirm = simpledialog.askstring(
                        'confirmar',
                        'Repite contraseña: ',
                        show='*',
                        parent=self.root
                    )

                    if nueva != confirm:
                        messagebox.showerror("Error", 'No coinciden', parent=self.root)
                        continue

                    Usuario.actualizar_password(resultado[0], nueva)

                    messagebox.showinfo("OK", 'Contraseña actualizada', parent=self.root)
                    break

                if resultado[3] == 'NOTIFICACION':
                    messagebox.showerror("Error", 'Usuario no valido')
                    return

            id_usuario, username, password, rol, primer_login = resultado

            self.root.destroy()

            # Abrir sistema principal
            from ui.main_app import Mainapp

            app = tk.Tk()
            Mainapp(app, rol)
            app.mainloop()

        except Exception as e:

            from tkinter import messagebox
            messagebox.showerror("Error conexion", str(e))

            # Regresar a config
            self.root.destroy()

            import tkinter as tk
            from ui.config_server import ConfigServidor

            root = tk.Tk()
            ConfigServidor(root)
            root.mainloop()

            return

    def abrir_config(self):

        from ui.config_server import ConfigServidor
        self.root.destroy()

        root = tk.Tk()
        ConfigServidor(root)
        root.mainloop()


