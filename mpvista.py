import os
import tkinter as tk
from tkinter import ttk
from principalvista import BASE_DIR

ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")

def crear_ventana(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Control de Materias Primas")
    ventana.state("zoomed")
    ventana.configure(bg="#ffffff")  # Unificado a tu fondo blanco
    ventana.transient(parent)
    ventana.grab_set()

    if os.path.exists(ICON_PATH):
        try:
            ventana.iconbitmap(ICON_PATH)
        except:
            pass
    return ventana

def crear_toolstrip(ventana, abrir_agregar=None, abrir_modificar=None, abrir_eliminar=None):
    toolstrip = tk.Frame(ventana, bg="#dde6ed")
    toolstrip.pack(fill=tk.X)

    fuente = ("Segoe UI", 12, "bold")
    fg = "#003366"
    bg = "#cfe2f3"
    hover = "#a4c2f4"

    def boton(texto, comando):
        return tk.Button(
            toolstrip, text=texto, font=fuente, fg=fg, bg=bg,
            activebackground=hover, activeforeground=fg,
            bd=0, relief="flat", command=comando
        )

    if abrir_agregar:
        boton("Agregar Material", abrir_agregar).pack(side=tk.LEFT, padx=10, pady=10)
    if abrir_modificar:
        boton("Modificar", abrir_modificar).pack(side=tk.LEFT, padx=10, pady=10)
    if abrir_eliminar:
        boton("Eliminar", abrir_eliminar).pack(side=tk.LEFT, padx=10, pady=10)

    boton("Cerrar", ventana.destroy).pack(side=tk.LEFT, padx=10, pady=10)
    tk.Frame(toolstrip, bg="#dde6ed").pack(side=tk.LEFT, expand=True, fill=tk.X)

def crear_filtro(ventana, callback_filtro):
    frame = tk.Frame(ventana, bg="#ffffff")
    frame.pack(fill=tk.X, padx=15, pady=(8, 5))

    tk.Label(
        frame, text="Filtrar por:", bg="#ffffff",
        font=("Segoe UI", 12, "bold"), fg="#003366"
    ).pack(side=tk.LEFT, padx=5)

    combo = ttk.Combobox(
        frame, state="readonly", width=25,
        values=["ID", "Nombre", "U. Medida", "Precio", "Stock"]
    )
    combo.set("Nombre")
    combo.pack(side=tk.LEFT, padx=8)

    entry = ttk.Entry(frame)
    entry.pack(side=tk.LEFT, padx=8, fill=tk.X, expand=True)

    entry.bind("<Return>", lambda e: callback_filtro(combo.get(), entry.get()))
    return combo, entry
def crear_tabla(ventana, filas_visibles=15):
    # Contenedor principal que NO se expande infinitamente hacia abajo
    contenedor = tk.Frame(ventana, bg="#ffffff")
    contenedor.pack(fill=tk.X, padx=20, pady=15)

    # Frame interno con un borde sutil para delimitar la tabla
    frame_tree = tk.Frame(contenedor, bg="#ffffff", highlightbackground="#cccccc", highlightthickness=1)
    frame_tree.pack(fill=tk.X, expand=True)

    # Definimos la cantidad de filas fijas visibles (ej: 15 filas)
    tree = ttk.Treeview(
        frame_tree,
        show="headings",
        height=filas_visibles
    )

    scroll_y = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=tree.yview)
    scroll_x = ttk.Scrollbar(frame_tree, orient=tk.HORIZONTAL, command=tree.xview)

    tree.configure(
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    # Ubicación con Grid dentro del marco contenedor
    tree.grid(row=0, column=0, sticky="ew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    frame_tree.grid_columnconfigure(0, weight=1)

    # Columnas
    tree["columns"] = ("ID", "Nombre", "Unidad Medida", "Precio Unitario")

    # Ajuste de anchos fijos proporcionales
    tree.column("ID", width=70, anchor="center")
    tree.column("Nombre", width=400, anchor="w")
    tree.column("Unidad Medida", width=150, anchor="center")
    tree.column("Precio Unitario", width=150, anchor="e")

    for c in tree["columns"]:
        tree.heading(c, text=c)

    # Estilos visuales del Treeview
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 11, "bold"),
        background="#d9e1f2",
        foreground="#003366",
        padding=5
    )

    style.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=28,
        background="white",
        fieldbackground="white"
    )

    # Color de selección
    style.map(
        "Treeview",
        background=[("selected", "#cfe2f3")],
        foreground=[("selected", "#003366")]
    )

    return tree