import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Configuración de rutas de archivos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")
FONDO_PATH = os.path.join(BASE_DIR, "fondo.jpg")

def crear_ventana_principal():
    root = tk.Tk()
    root.title("Gestión de Tornería - Presupuestos y Materiales")
    root.state("zoomed")
    # CAMBIO: Ventana con fondo blanco puro para unificar con el logo
    root.configure(bg="#ffffff")

    # Intentar cargar el ícono de la ventana
    if os.path.exists(ICON_PATH):
        try:
            root.iconbitmap(ICON_PATH)
        except:
            pass

    # --- Lógica de Fondo Centrado y Proporcional ---
    if os.path.exists(FONDO_PATH):
        try:
            img_original = Image.open(FONDO_PATH)
            ancho_orig, alto_orig = img_original.size
            proporcion_orig = ancho_orig / alto_orig

            # CAMBIO: Contenedor con fondo blanco puro (#ffffff)
            fondo_label = tk.Label(root, bg="#ffffff")
            fondo_label.place(relx=0, rely=0, relwidth=1, relheight=1)

            def actualizar_fondo(event=None):
                ancho_ventana = root.winfo_width()
                alto_ventana = root.winfo_height()
                
                if ancho_ventana > 100 and alto_ventana > 100:
                    proporcion_ventana = ancho_ventana / alto_ventana
                    
                    if proporcion_ventana > proporcion_orig:
                        nuevo_alto = alto_ventana
                        nuevo_ancho = int(alto_ventana * proporcion_orig)
                    else:
                        nuevo_ancho = ancho_ventana
                        nuevo_alto = int(ancho_ventana / proporcion_orig)
                    
                    img_reseteada = img_original.resize((nuevo_ancho, nuevo_alto), Image.Resampling.LANCZOS)
                    root.photo_fondo = ImageTk.PhotoImage(img_reseteada)
                    fondo_label.config(image=root.photo_fondo)

            root.bind("<Configure>", actualizar_fondo)
        except Exception as e:
            print(f"Error al cargar fondo: {e}")

    return root

def configurar_estilos(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    # Estilo para los botones principales de la tornería
    style.configure(
        "TButton",
        font=("Segoe UI", 13, "bold"),
        padding=12,
        foreground="#004080",
        background="#cce6ff"
    )

    style.map(
        "TButton",
        foreground=[("active", "#00264d")],
        background=[("active", "#99ccff")]
    )

    # Estilo diferenciado y llamativo para el botón de Salida
    style.configure(
        "Salir.TButton",
        font=("Segoe UI", 13, "bold"),
        padding=12,
        foreground="#800000",
        background="#ffcccc"
    )
    style.map(
        "Salir.TButton",
        foreground=[("active", "#4d0000")],
        background=[("active", "#ff9999")]
    )

def crear_botones(root, abrir_presupuestos, abrir_materias_primas, abrir_clientes, comando_salir):
    # Frame de la barra superior (gris intermedio como el de tu captura original)
    button_frame = tk.Frame(root, bg="#999a9c", height=70)
    button_frame.pack(side="top", fill="x")

    # Lista de botones dinámicos de gestión
    config_botones = [
        ("Presupuestos", abrir_presupuestos),
        ("Materias Primas", abrir_materias_primas),
        ("Clientes", abrir_clientes)
    ]

    # Generar y posicionar los botones uno al lado del otro
    for i, (texto, comando) in enumerate(config_botones):
        btn = ttk.Button(button_frame, text=texto, command=comando)
        btn.grid(row=0, column=i, padx=15, pady=10, sticky="nsew")
        button_frame.columnconfigure(i, weight=1)

    # Posicionar el botón Salir en la última columna de la derecha
    col_salir = len(config_botones)
    btn_salir = ttk.Button(button_frame, text="Salir", command=comando_salir, style="Salir.TButton")
    btn_salir.grid(row=0, column=col_salir, padx=15, pady=10, sticky="nsew")
    button_frame.columnconfigure(col_salir, weight=1)

    return button_frame