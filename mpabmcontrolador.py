import tkinter as tk
from tkinter import messagebox
import mpabmvista as vista
from mpabmmodelo import (
    insertar_materia_prima,
    actualizar_materia_prima,
    obtener_proximo_id
)

def iniciar_mpabm(parent, conexion, estado="AGREGAR", datos_mp=None):
    guardado_exitoso = [False] # Estado que retornaremos al controlador principal

    def guardar():
        try:
            datos = {}
            for campo_bd, widget in campos.items():
                if campo_bd == "id_material":
                    continue
                
                valor = widget.get().strip()
                
                # Validación del campo numérico de precio
                if campo_bd == "precio_unitario":
                    try:
                        valor = float(valor.replace(",", "."))
                    except ValueError:
                        messagebox.showerror("Error de formato", "Por favor, ingrese un precio unitario válido.", parent=ventana)
                        return
                
                if not valor and campo_bd == "nombre":
                    messagebox.showwarning("Faltan datos", "El nombre del material es obligatorio.", parent=ventana)
                    return

                datos[campo_bd] = valor

            if estado == "AGREGAR":
                insertar_materia_prima(conexion, datos)
                mensaje = "Materia prima agregada correctamente."
            else:
                actualizar_materia_prima(conexion, datos_mp["id_material"], datos)
                mensaje = "Materia prima modificada correctamente."

            messagebox.showinfo("Éxito", mensaje, parent=ventana)
            guardado_exitoso[0] = True
            ventana.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}", parent=ventana)

    # Inicializar la interfaz del formulario
    ventana = vista.crear_ventana(parent)

    vista.crear_toolstrip(
        ventana=ventana,
        estado_texto="Nueva Materia Prima" if estado == "AGREGAR" else "Modificando Material",
        comando_guardar=guardar,
        comando_cancelar=ventana.destroy
    )

    campos = vista.crear_formulario(ventana)

    # --- MODO AGREGAR ---
    if estado == "AGREGAR":
        proximo_id = obtener_proximo_id(conexion)
        if "id_material" in campos:
            campos["id_material"].config(state="normal")
            campos["id_material"].insert(0, str(proximo_id))
            campos["id_material"].config(state="readonly")

    # --- MODO MODIFICAR ---
    if estado == "MODIFICAR" and datos_mp:
        for campo_bd, valor in datos_mp.items():
            if campo_bd not in campos:
                continue

            widget = campos[campo_bd]
            
            if isinstance(widget, tk.Combobox):
                widget.set(valor)
            else:
                widget.config(state="normal")
                widget.delete(0, tk.END)
                widget.insert(0, str(valor))

        if "id_material" in campos:
            campos["id_material"].config(state="readonly")

    ventana.wait_window()  # Espera a que se cierre para retornar el resultado
    return guardado_exitoso[0]