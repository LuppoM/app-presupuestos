import tkinter as tk
from tkinter import ttk
from principalvista import BASE_DIR
import os

# Ruta del ícono de la aplicación
ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")


# ============================================================
# VENTANA PRINCIPAL DEL ABM
# ============================================================
def crear_ventana(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Formulario de Materia Prima")
    ventana.geometry("550x400")
    ventana.configure(bg="#ffffff")  # Fondo blanco limpio para el taller
    ventana.resizable(False, False)
    ventana.transient(parent)
    ventana.grab_set()

    if os.path.exists(ICON_PATH):
        try:
            ventana.iconbitmap(ICON_PATH)
        except:
            pass

    return ventana


# ============================================================
# BARRA DE ACCIONES (TOOLSTRIP)
# ============================================================
def crear_toolstrip(ventana, estado_texto, comando_guardar, comando_cancelar):
    barra = tk.Frame(ventana, bg="#dde6ed", height=55)
    barra.pack(fill=tk.X)
    barra.pack_propagate(False)

    # Etiqueta del estado actual (Nueva / Modificando)
    tk.Label(
        barra,
        text=estado_texto,
        bg="#dde6ed",
        fg="#003366",
        font=("Segoe UI", 11, "bold")
    ).pack(side=tk.LEFT, padx=15)

    # Botón Cancelar - Corrección para Python 3.7 (padx/pady en lugar de padding)
    tk.Button(
        barra,
        text="Cancelar",
        font=("Segoe UI", 10, "bold"),
        bg="#ffc7ce",
        fg="#9c0006",
        bd=0,
        padx=10,
        pady=4,
        command=comando_cancelar
    ).pack(side=tk.RIGHT, padx=15, pady=8)

    # Botón Guardar - Corrección para Python 3.7 (padx/pady en lugar de padding)
    tk.Button(
        barra,
        text="Guardar",
        font=("Segoe UI", 10, "bold"),
        bg="#c6efce",
        fg="#006100",
        bd=0,
        padx=10,
        pady=4,
        command=comando_guardar
    ).pack(side=tk.RIGHT, pady=8)


# ============================================================
# FORMULARIO DE CAPTURA (SIN COLUMNA STOCK)
# ============================================================
def crear_formulario(ventana):
    contenedor = tk.Frame(ventana, bg="#ffffff")
    contenedor.pack(fill="both", expand=True, padx=30, pady=25)

    entradas = {}
    
    # Mapeo descriptivo -> Nombre real en la base de datos de tornería
    campos = [
        ("ID Material", "id_material"),
        ("Nombre", "nombre"),
        ("Unidad de Medida", "unidad_medida"),
        ("Precio Unitario", "precio_unitario")
    ]

    for fila, (label_texto, campo_bd) in enumerate(campos):
        tk.Label(
            contenedor,
            text=f"{label_texto}:",
            bg="#ffffff",
            font=("Segoe UI", 11, "bold"),
            fg="#003366"
        ).grid(row=fila, column=0, sticky="w", pady=12)

        # Configuración selectiva de los tipos de control
        if campo_bd == "unidad_medida":
            # Combobox para estandarizar las compras y formatos del taller
            widget = ttk.Combobox(
                contenedor, 
                width=32, 
                state="readonly", 
                values=["Metros", "Unidades", "Kilos", "Barras", "Placas"]
            )
            widget.set("Metros")
        else:
            widget = ttk.Entry(contenedor, width=35, font=("Segoe UI", 10))

        widget.grid(row=fila, column=1, pady=12, padx=15, sticky="w")

        # El ID es gestionado automáticamente por la base de datos
        if campo_bd == "id_material":
            widget.configure(state="readonly")

        entradas[campo_bd] = widget

    return entradas