# abmpresupuestoscontrolador.py
from tkinter import messagebox
import tkinter as tk
from abmpresupuestosmodelo import ABMPresupuestosModelo
import abmpresupuestosvista as vista

class ABMPresupuestosControlador:
    def __init__(self, parent, conexion, estado, datos_presupuesto):
        self.estado = estado
        self.id_presupuesto = datos_presupuesto  # Guardamos el ID seleccionado (ej. seleccionado del Treeview)
        self.modelo = ABMPresupuestosModelo(conexion)
        self.guardado_exitoso = False
        
        self.materiales_disponibles = self.modelo.obtener_materias_primas()
        self.detalles_locales = []

        # Instanciar la interfaz del ABM
        self.ventana = vista.crear_ventana(parent)
        
        titulo_banner = "Modificar Presupuesto" if self.estado == "MODIFICAR" else "Nuevo Presupuesto de Taller"
        vista.crear_toolstrip(self.ventana, comando_guardar=self.guardar, titulo=titulo_banner)
        
        self.campos_cabecera = vista.crear_formulario_cabecera(self.ventana)
        self.tree_detalles = vista.crear_seccion_detalles(self.ventana, self.abrir_seleccion, self.quitar_material)
        self.ent_mo, self.lbl_mat, self.lbl_gen = vista.crear_panel_totales(self.ventana, self.recalcular_totales)

        # SI VIENE EN MODO MODIFICAR, CARGAMOS LOS DATOS EN LOS CAMPOS
        if self.estado == "MODIFICAR" and self.id_presupuesto:
            self.cargar_datos_existentes()

    def cargar_datos_existentes(self):
        cabecera = self.modelo.obtener_por_id(self.id_presupuesto)
        if cabecera:
            self.campos_cabecera["fecha"].delete(0, tk.END)
            self.campos_cabecera["fecha"].insert(0, cabecera["fecha"])

            self.campos_cabecera["cliente"].delete(0, tk.END)
            self.campos_cabecera["cliente"].insert(0, cabecera["cliente"])

            self.campos_cabecera["descripcion"].delete(0, tk.END)
            self.campos_cabecera["descripcion"].insert(0, cabecera["descripcion"])

            self.ent_mo.delete(0, tk.END)
            self.ent_mo.insert(0, f"{cabecera['mano_obra']:.2f}")

            # Traer los materiales asociados
            self.detalles_locales = self.modelo.obtener_detalles_por_id(self.id_presupuesto)
            self.recalcular_totales()

    def abrir_seleccion(self):
        if not self.materiales_disponibles:
            messagebox.showwarning("Catálogo vacío", "Debe cargar materias primas en el sistema antes de presupuestar.", parent=self.ventana)
            return
        vista.crear_ventana_seleccion_material(self.ventana, self.materiales_disponibles, self.confirmar_adicion_material)

    def confirmar_adicion_material(self, nombre_seleccionado, cantidad_texto, sub_ventana):
        try:
            cantidad = float(cantidad_texto.replace(",", "."))
            if cantidad <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error de cantidad", "Ingrese un valor numérico mayor a cero.", parent=sub_ventana)
            return

        mat_info = next(m for m in self.materiales_disponibles if m["nombre"] == nombre_seleccionado)

        self.detalles_locales.append({
            "id_material": mat_info["id_material"],
            "nombre": mat_info["nombre"],
            "unidad": mat_info["text_unidad"] if "text_unidad" in mat_info else mat_info["unidad_medida"],
            "precio_venta": mat_info["precio_unitario"],
            "cantidad": cantidad,
            "subtotal": cantidad * mat_info["precio_unitario"]
        })

        self.recalcular_totales()
        sub_ventana.destroy()

    def quitar_material(self):
        seleccionado = self.tree_detalles.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un material de la grilla para removerlo.", parent=self.ventana)
            return
        
        self.detalles_locales.pop(int(seleccionado))
        self.recalcular_totales()

    def recalcular_totales(self):
        self.tree_detalles.delete(*self.tree_detalles.get_children())
        subtotal_materiales = 0.0

        for idx, item in enumerate(self.detalles_locales):
            self.tree_detalles.insert(
                "", "end", iid=str(idx),
                values=(item["nombre"], f"{item['cantidad']:.2f} {item['unidad']}", f"$ {item['precio_venta']:.2f}", f"$ {item['subtotal']:.2f}")
            )
            subtotal_materiales += item["subtotal"]

        try:
            mano_obra = float(self.ent_mo.get().replace(",", "."))
            if mano_obra < 0: mano_obra = 0.0
        except ValueError:
            mano_obra = 0.0

        total_general = subtotal_materiales + mano_obra

        self.lbl_mat.config(text=f"Materiales: $ {subtotal_materiales:.2f}")
        self.lbl_gen.config(text=f"TOTAL: $ {total_general:.2f}")

        return subtotal_materiales, mano_obra, total_general

    def guardar(self):
        cliente = self.campos_cabecera["cliente"].get().strip()
        descripcion = self.campos_cabecera["descripcion"].get().strip()
        fecha = self.campos_cabecera["fecha"].get().strip()

        if not cliente:
            messagebox.showwarning("Faltan Datos", "El nombre del cliente es obligatorio.", parent=self.ventana)
            return
        if not descripcion:
            messagebox.showwarning("Faltan Datos", "Por favor ingrese una breve descripción del trabajo.", parent=self.ventana)
            return

        sub_mat, mo, total = self.recalcular_totales()

        cabecera = {
            "fecha": fecha,
            "cliente": cliente,
            "descripcion": descripcion,
            "mano_obra": mo,
            "total_materiales": sub_mat,
            "total_general": total
        }

        # Guardar según el estado
        if self.estado == "MODIFICAR":
            exito = self.modelo.actualizar_presupuesto(self.id_presupuesto, cabecera, self.detalles_locales)
        else:
            exito = self.modelo.guardar_presupuesto(cabecera, self.detalles_locales)

        if exito:
            messagebox.showinfo("Éxito", "Presupuesto guardado con éxito.", parent=self.ventana)
            self.guardado_exitoso = True
            self.ventana.destroy()
        else:
            messagebox.showerror("Error", "Ocurrió un error al intentar escribir el presupuesto.", parent=self.ventana)