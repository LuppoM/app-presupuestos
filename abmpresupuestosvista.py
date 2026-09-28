import os
import datetime
import tkinter as tk
from tkinter import ttk

def _aplicar_icono(ventana):
    """Aplica el ícono de la aplicación a la ventana especificada si existe el archivo."""
    if os.path.exists("iconom.ico"):
        try:
            ventana.iconbitmap("iconom.ico")
        except Exception:
            pass

def crear_ventana(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Formulario de Presupuesto")
    
    # Maximizar según sistema operativo
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

def crear_toolstrip(ventana, comando_guardar, titulo="Nuevo Presupuesto de Taller"):
    barra = tk.Frame(ventana, bg="#dde6ed", height=50)
    barra.pack(fill=tk.X, side=tk.TOP)
    barra.pack_propagate(False)

    tk.Label(
        barra, text=titulo, 
        bg="#dde6ed", fg="#003366", font=("Segoe UI", 11, "bold")
    ).pack(side=tk.LEFT, padx=15)

    tk.Button(
        barra, text="Cancelar", font=("Segoe UI", 10, "bold"),
        bg="#ffc7ce", fg="#9c0006", bd=0, padx=12, pady=4,
        command=ventana.destroy
    ).pack(side=tk.RIGHT, padx=15, pady=6)

    tk.Button(
        barra, text="Guardar Presupuesto", font=("Segoe UI", 10, "bold"),
        bg="#c6efce", fg="#006100", bd=0, padx=12, pady=4,
        command=comando_guardar
    ).pack(side=tk.RIGHT, pady=6)

def crear_formulario_cabecera(ventana):
    contenedor = tk.LabelFrame(
        ventana, text=" Datos del Trabajo / Cliente ", 
        bg="#ffffff", font=("Segoe UI", 10, "bold"), fg="#003366"
    )
    contenedor.pack(fill=tk.X, padx=20, pady=10, ipady=5)

    entradas = {}
    fecha_hoy = datetime.datetime.now().strftime("%d/%m/%Y")

    contenedor.columnconfigure(3, weight=1)

    # Fila 0: Fecha y Cliente
    tk.Label(contenedor, text="Fecha:", bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=15, pady=5)
    ent_fecha = ttk.Entry(contenedor, width=12, font=("Segoe UI", 10))
    ent_fecha.insert(0, fecha_hoy)
    ent_fecha.grid(row=0, column=1, sticky="w", pady=5, padx=(0, 20))
    entradas["fecha"] = ent_fecha

    tk.Label(contenedor, text="Cliente:", bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, sticky="w", padx=15, pady=5)
    ent_cliente = ttk.Entry(contenedor, font=("Segoe UI", 10))
    ent_cliente.grid(row=0, column=3, sticky="ew", pady=5, padx=(0, 15))
    entradas["cliente"] = ent_cliente

    # Fila 1: Descripción
    tk.Label(contenedor, text="Trabajo:", bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", padx=15, pady=5)
    ent_desc = ttk.Entry(contenedor, font=("Segoe UI", 10))
    ent_desc.grid(row=1, column=1, columnspan=3, sticky="ew", pady=5, padx=(0, 15))
    entradas["descripcion"] = ent_desc

    return entradas

def crear_seccion_detalles(ventana, comando_agregar, comando_quitar):
    # Panel de botones intermedio
    frame_acciones = tk.Frame(ventana, bg="#ffffff")
    frame_acciones.pack(fill=tk.X, padx=20, pady=(5, 0))

    tk.Button(
        frame_acciones, text="Añadir Material", font=("Segoe UI", 9, "bold"),
        bg="#d9e1f2", fg="#003366", bd=0, padx=10, pady=4, command=comando_agregar
    ).pack(side=tk.LEFT, padx=2)

    tk.Button(
        frame_acciones, text="Quitar Material", font=("Segoe UI", 9, "bold"),
        bg="#ffc7ce", fg="#9c0006", bd=0, padx=10, pady=4, command=comando_quitar
    ).pack(side=tk.LEFT, padx=5)

    # Contenedor de la Grilla (Compacto)
    frame_tabla = tk.Frame(ventana, bg="#ffffff")
    frame_tabla.pack(fill=tk.X, padx=20, pady=5)

    scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical")
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 'height=6' define que se muestren solo 6 filas visibles
    tree = ttk.Treeview(
        frame_tabla, 
        columns=("Mat", "Cant", "Prec", "Sub"), 
        show="headings",
        height=6,
        yscrollcommand=scrollbar.set
    )
    scrollbar.config(command=tree.yview)

    # Anchos equilibrados
    tree.column("Mat", width=400, minwidth=200, anchor="w", stretch=True)
    tree.column("Cant", width=100, minwidth=80, anchor="center", stretch=False)
    tree.column("Prec", width=120, minwidth=90, anchor="e", stretch=False)
    tree.column("Sub", width=120, minwidth=90, anchor="e", stretch=False)

    tree.heading("Mat", text="Material Seleccionado")
    tree.heading("Cant", text="Cantidad")
    tree.heading("Prec", text="Precio Unit.")
    tree.heading("Sub", text="Subtotal")
    
    tree.pack(side=tk.LEFT, fill=tk.X, expand=True)

    return tree

def crear_panel_totales(ventana, comando_recalcular):
    frame_totales = tk.LabelFrame(
        ventana, text=" Costos y Totales Finales ", 
        bg="#ffffff", font=("Segoe UI", 10, "bold"), fg="#003366"
    )
    frame_totales.pack(fill=tk.X, padx=20, pady=(5, 15), ipady=5)

    # Costo Mano de obra
    tk.Label(frame_totales, text="Mano de Obra (Taller): $", bg="#ffffff", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=15, pady=5)
    ent_mo = ttk.Entry(frame_totales, width=12, font=("Segoe UI", 10, "bold"))
    ent_mo.insert(0, "0.00")
    ent_mo.grid(row=0, column=1, sticky="w", pady=5)
    
    # Botón de cálculo
    tk.Button(
        frame_totales, text="Calcular", font=("Segoe UI", 9, "bold"), 
        bg="#eeeeee", fg="#333333", bd=1, command=comando_recalcular
    ).grid(row=0, column=2, padx=10)

    # Etiquetas de totales
    lbl_mat = tk.Label(frame_totales, text="Materiales: $ 0.00", bg="#ffffff", fg="#444444", font=("Segoe UI", 10, "bold"))
    lbl_mat.grid(row=0, column=3, sticky="e", padx=20)

    lbl_gen = tk.Label(frame_totales, text="TOTAL: $ 0.00", bg="#ffffff", fg="#003366", font=("Segoe UI", 12, "bold"))
    lbl_gen.grid(row=0, column=4, sticky="e", padx=20)

    frame_totales.columnconfigure(3, weight=1)
    frame_totales.columnconfigure(4, weight=1)

    return ent_mo, lbl_mat, lbl_gen

def crear_ventana_seleccion_material(parent, lista_materiales, comando_confirmar):
    sub = tk.Toplevel(parent)
    sub.title("Añadir Elemento")
    sub.geometry("420x230")
    sub.configure(bg="#ffffff")
    sub.resizable(False, False)
    sub.transient(parent)
    sub.grab_set()

    _aplicar_icono(sub)

    tk.Label(sub, text="Seleccione el Material:", bg="#ffffff", font=("Segoe UI", 10, "bold"), fg="#003366").pack(anchor="w", padx=25, pady=(20, 5))
    
    nombres = [m["nombre"] for m in lista_materiales]
    combo = ttk.Combobox(sub, values=nombres, state="readonly", width=42, font=("Segoe UI", 10))
    if nombres: 
        combo.set(nombres[0])
    combo.pack(padx=25, pady=5)

    tk.Label(sub, text="Cantidad a utilizar:", bg="#ffffff", font=("Segoe UI", 10, "bold"), fg="#003366").pack(anchor="w", padx=25, pady=5)
    ent_cant = ttk.Entry(sub, width=15, font=("Segoe UI", 10))
    ent_cant.insert(0, "1.00")
    ent_cant.pack(anchor="w", padx=25, pady=5)

    tk.Button(
        sub, text="Inyectar al Presupuesto", font=("Segoe UI", 10, "bold"),
        bg="#c6efce", fg="#006100", bd=0, padx=15, pady=5,
        command=lambda: comando_confirmar(combo.get(), ent_cant.get(), sub)
    ).pack(pady=20)