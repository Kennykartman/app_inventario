import tkinter as tk
from utils.estilos import *

def contenedor(root):

    frame =tk.Frame(root,bg=COLOR_BG)
    frame.pack(fill='both', expand=True, padx=20, pady=20)

    return frame

