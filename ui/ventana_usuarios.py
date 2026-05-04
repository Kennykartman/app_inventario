import tkinter as tk
from threading import activeCount
from tkinter import messagebox, ttk, simpledialog

from models.usuario import Usuario
from utils.security import validar_password
from utils.exportar_excel import exportar_treeview
class VentanaUsuario:

    def __init__(self,root):

        self.root = tk.Toplevel(root)
        self.root.title('Usuarios')
        self.root.geometry('1000x700')



        #Campos
        tk.Label(self.root,text='Usuario').pack()
        self.username = tk.Entry(self.root)
        self.username.pack()

        tk.Label(self.root, text='Contraseña').pack()
        self.password = tk.Entry(self.root)
        self.password.pack()

        tk.Label(self.root, text='Email').pack()
        self.email = tk.Entry(self.root)
        self.email.pack()

        tk.Label(self.root, text='Rol').pack()
        self.rol = ttk.Combobox(
            self.root,
            values=['ADMIN','OPERADOR', 'NOTIFICACION'],
            state='readonly'
        )
        self.rol.pack()
        self.rol.bind('<<ComboboxSelected>>', self.on_rol_change)

        tk.Button(
            self.root,
            text='Crear Usuario',
            command=self.crear_usuario
        ).pack(pady=10)

        self.username.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.rol.set('')

        self.password.config(state='normal')

        # Tabla
        self.tabla =ttk.Treeview(
            self.root,
            columns=('ID', 'Usuario', 'Rol', 'Email'),
            show='headings',
        )

        for col in ('ID', 'Usuario', 'Rol', 'Email'):
            self.tabla.heading(col, text=col)

        self.tabla.pack(fill='both', expand=True)

        self.cargar_usuarios()

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


        tk.Button(
            self.root,
            text='Cambiar contraseña',
            command=self.cambiar_password
        ).pack()

    def crear_usuario(self):

        user = self.username.get()
        pwd = self.password.get()
        rol = self.rol.get()
        email = self.email.get()

        if not user or not rol:
            messagebox.showwarning('Aviso', 'Los campos son obligatorios')
            return

        if rol == 'NOTIFICACION':
            self.password.config(state='disabled')
        else:
            self.password.config(state='normal')

        Usuario.crear(user, pwd, rol, email)

        self.cargar_usuarios()

        messagebox.showinfo('Usuario', 'Usuario creado correctamente')

    def cargar_usuarios(self):

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        usuarios = Usuario.listar()

        for u in usuarios:
            self.tabla.insert('', 'end', values=u)

    def cambiar_password(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning('Aviso', 'Selecciona un usuario')
            return

        datos = self.tabla.item(seleccionado)['values']
        id_usuario = datos[0]

        nueva = simpledialog.askstring(
            'Nueva contraseña',
            'Ingresa nueva contraseña: ',
            show='*',
            parent=self.root
        )

        if not nueva:
            return

        valido, msg = validar_password(nueva)

        if not valido:
            messagebox.showwarning('Error', msg, parent=self.root)
            return

        confirm = simpledialog.askstring(
            'Confirmar',
            'Repite contraseña: ',
            show='*',
            parent=self.root
        )

        if nueva != confirm:
            messagebox.showerror('Error', 'No coinciden')
            return

        from models.usuario import Usuario
        Usuario.actualizar_password(id_usuario, nueva)
        messagebox.showinfo('ok', 'Contraseña actualizada')

    def on_rol_change(self, event=None):

        rol = self.rol.get()

        if rol == 'NOTIFICACION':
            self.password.delete(0, tk.END)
            self.password.config(state='disabled')
        else:
            self.password.config(state='normal')

        self.root.update_idletasks()


