# utils/componentes

import tkinter as tk
from utils.estilos import *

def boton(parent, texto,  comando, color=COLOR_PRIMARIO):

    return tk.Button(
        parent,
        text=texto,
        command=comando,
        bg=color,
        fg='white',
        font=FUENTE_BOTON,
        relief='flat',
        padx=10,
        pady=5,
        cursor='hand2'
    )

def titulo(parent,texto):

    return tk.Label(
        parent,
        text=texto,
        bg=COLOR_BG,
        fg=COLOR_TEXTO,
        font=FUENTE_TITULO
    )

def card(parent):

    frame = tk.Frame(
        parent,
        bg=COLOR_CARD,
        bd=0,
        highlightbackground='#dcdde1',
        highlightthickness=1,
    )

    return frame

def boton_secundario(parent, texto, comando):

    return tk.Button(
        parent,
        text=texto,
        command=comando,
        bg='#ecf0f1',
        fg='#2c3e50',
        font=('Sagoe UI', 9),
        relief='flat',
        padx=8,
        pady=4,
        cursor='hand2'
        )