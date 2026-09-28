import os
import tkinter as tk
from tkinter import ttk

def _aplicar_icono(ventana):
    """Aplica el ícono iconom.ico a la ventana si existe."""
    if os.path.exists("iconom.ico"):
        try:
            ventana.iconbitmap("iconom.ico")
        except Exception:
            pass

def crear_ventana(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Control de Presupuestos - Taller")
    
    # Maximizar la ventana para ocupar toda la pantalla
    try:
        ventana.state("zoomed")
    except Exception:
        ancho = ventana.winfo_screenwidth()
        alto = ventana.winfo_screenheight()
        ventana.geometry(f"{ancho}x{alto}+0+0")

    ventana.configure(bg="#ffffff")
    ventana.transient(parent)
    ventana.grab_set()
    
    _aplicar_icono(ventana)
    return ventana

def crear_toolstrip(ventana, abrir_agregar, abrir_modificar, abrir_eliminar, comando_imprimir):
    barra = tk.Frame(ventana, bg="#dde6ed", height=50)
    barra.pack(fill=tk.X, side=tk.TOP)
    barra.pack_propagate(False)

    # Botón Nuevo Presupuesto
    tk.Button(
        barra, text="Nuevo Presupuesto", 
        font=("Segoe UI", 10, "bold"), bg="#cfe2f3", fg="#003366", 
        bd=0, padx=12, pady=4, command=abrir_agregar
    ).pack(side=tk.LEFT, padx=10, pady=8)

    # Botón Modificar
    tk.Button(
        barra, text="Modificar", 
        font=("Segoe UI", 10, "bold"), bg="#fff2cc", fg="#7f6000", 
        bd=0, padx=12, pady=4, command=abrir_modificar
    ).pack(side=tk.LEFT, padx=5, pady=8)

    # Botón Eliminar
    tk.Button(
        barra, text="Eliminar", 
        font=("Segoe UI", 10, "bold"), bg="#ffc7ce", fg="#9c0006", 
        bd=0, padx=12, pady=4, command=abrir_eliminar
    ).pack(side=tk.LEFT, padx=5, pady=8)

    # Botón Imprimir
    tk.Button(
        barra, text="Imprimir", 
        font=("Segoe UI", 10, "bold"), bg="#2b579a", fg="#ffffff", 
        bd=0, padx=12, pady=4, command=comando_imprimir
    ).pack(side=tk.LEFT, padx=5, pady=8)

    # Botón Cerrar
    tk.Button(
        barra, text="Cerrar", 
        font=("Segoe UI", 10, "bold"), bg="#eeeeee", fg="#333333", 
        bd=0, padx=12, pady=4, command=ventana.destroy
    ).pack(side=tk.LEFT, padx=10, pady=8)

def crear_tabla(ventana):
    # Contenedor con un alto dominante pero holgado (fill=tk.X con pad vertical)
    frame_grid = tk.Frame(ventana, bg="#ffffff")
    frame_grid.pack(fill=tk.X, expand=False, padx=20, pady=(15, 30), side=tk.TOP)

    scrollbar = ttk.Scrollbar(frame_grid, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Aumentamos a height=22 para que cubra la mayor parte de la pantalla
    tree = ttk.Treeview(
        frame_grid, 
        columns=("ID", "Fecha", "Cliente", "Detalle", "Total"), 
        show="headings",
        height=22,
        yscrollcommand=scrollbar.set
    )
    scrollbar.config(command=tree.yview)

    # Anchos de columnas ajustados
    tree.column("ID", width=80, anchor="center")
    tree.column("Fecha", width=110, anchor="center")
    tree.column("Cliente", width=250, anchor="w")
    tree.column("Detalle", width=450, anchor="w")
    tree.column("Total", width=140, anchor="e")

    tree.heading("ID", text="N° Presup.")
    tree.heading("Fecha", text="Fecha")
    tree.heading("Cliente", text="Cliente")
    tree.heading("Detalle", text="Descripción del Trabajo")
    tree.heading("Total", text="Total General")

    tree.pack(side=tk.LEFT, fill=tk.X, expand=True)
    return tree