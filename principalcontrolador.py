from principalmodelo import obtener_conexion, realizar_backup
from tkinter import messagebox
import presupuestos
# Aquí irán las importaciones de tus módulos de tornería cuando los tengas listos:
import mp

def inicializar_app(vista):
    # 1. Preparar la ventana principal
    root = vista.crear_ventana_principal()
    vista.configurar_estilos(root)

    # 2. Conexión única para toda la sesión
    conexion = obtener_conexion()

    # --- LÓGICA DE INACTIVIDAD (10 MINUTOS) ---
    TIEMPO_LIMITE_MS = 10 * 60 * 1000  
    id_timer = [None] 

    def reset_timer(event=None):
        """Reinicia el contador de cierre cada vez que el usuario realiza una acción"""
        if id_timer[0]:
            root.after_cancel(id_timer[0])
        # Si pasan 10 min sin actividad, se dispara el cierre automático
        id_timer[0] = root.after(TIEMPO_LIMITE_MS, lambda: salir(automatico=True))

    # Detectar actividad en cualquier parte de la pantalla
    root.bind_all("<Any-KeyPress>", reset_timer)
    root.bind_all("<Any-ButtonPress>", reset_timer)
    root.bind_all("<Motion>", reset_timer)

    # --- FUNCIONES DE NAVEGACIÓN (TORNERÍA) ---
    def abrir_presupuestos():
        reset_timer()
        presupuestos.abrir_presupuestos(root,conexion)

        # presupuestos.abrir_modulo(root, conexion)

    def abrir_materias_primas():
        reset_timer()
        mp.abrir_mp(root,conexion)

    def abrir_clientes():
        reset_timer()
        print("Abriendo módulo de Clientes...")
        # clientes.abrir_modulo(root, conexion)

    # --- CIERRE SEGURO ---
    def salir(automatico=False):
        if not automatico:
            if not messagebox.askyesno("Salir", "¿Desea cerrar el sistema?\nSe realizará una copia de seguridad automática."):
                return

        try:
            # Primero cerramos conexión para liberar el archivo .db o la base de datos
            if conexion:
                conexion.close()
            
            # Ejecución del Backup de la tornería
            exito, mensaje = realizar_backup()
            
            if not exito and not automatico:
                messagebox.showwarning("Copia de seguridad", f"Atención: No se pudo realizar el backup.\n{mensaje}")
            elif automatico:
                print("Cierre automático por inactividad. Backup realizado.")

        except Exception as e:
            if not automatico:
                messagebox.showerror("Error al cerrar", f"Ocurrió un error: {e}")
        finally:
            root.destroy()

    # --- ARMADO DE INTERFAZ ---
    # Llamamos a la vista pasando exactamente los argumentos que configuramos antes
    vista.crear_botones(
        root, 
        abrir_presupuestos=abrir_presupuestos, 
        abrir_materias_primas=abrir_materias_primas, 
        abrir_clientes=abrir_clientes, 
        comando_salir=lambda: salir(False)
    )
    
    # Manejar el cierre desde la "X" superior de la ventana
    root.protocol("WM_DELETE_WINDOW", lambda: salir(False))
    
    # Iniciar el temporizador por primera vez
    reset_timer()

    # Lanzar el bucle principal de Tkinter
    root.mainloop()