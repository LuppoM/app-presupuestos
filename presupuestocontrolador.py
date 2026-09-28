import os
from tkinter import messagebox
from presupuestosmodelo import PresupuestosModelo
import presupuestosvista as vista
from abmpresupuestos import iniciar_presupuesto_abm 

# Importación del generador PDF
try:
    from pdf import generar_pdf_presupuesto
except ImportError:
    from pdf import generar_pdf_presupuesto

class PresupuestosControlador:
    def __init__(self, parent, conexion):
        self.parent = parent
        self.modelo = PresupuestosModelo(conexion)
        self.ventana = vista.crear_ventana(parent)

        # Configuramos la botonera superior
        vista.crear_toolstrip(
            self.ventana,
            abrir_agregar=self.agregar,
            abrir_modificar=self.modificar,
            abrir_eliminar=self.eliminar,
            comando_imprimir=self.imprimir
        )

        # Inicializamos el Treeview y cargamos datos
        self.tree = vista.crear_tabla(self.ventana)
        
        # Permitir modificar al hacer doble clic en una fila
        self.tree.bind("<Double-1>", lambda event: self.modificar())
        
        self.cargar()

    def cargar(self):
        """Limpia el Treeview y recarga los presupuestos desde la BD."""
        self.tree.delete(*self.tree.get_children())
        registros = self.modelo.obtener_todos()
        for r in registros:
            self.tree.insert(
                "",
                "end",
                iid=r["id"],
                values=(
                    r["id"], 
                    r["fecha"], 
                    r["cliente"], 
                    r["descripcion"], 
                    f"$ {r['total_general']:.2f}"
                )
            )

    def agregar(self):
        """Abre la subventana ABM para crear un presupuesto nuevo."""
        guardado = iniciar_presupuesto_abm(self.ventana, self.modelo.conexion, estado="AGREGAR")
        if guardado:
            self.cargar()

    def modificar(self):
        """Abre el formulario ABM cargando el registro seleccionado."""
        seleccionado = self.tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un presupuesto para modificar.", parent=self.ventana)
            return

        guardado = iniciar_presupuesto_abm(
            self.ventana, 
            self.modelo.conexion, 
            estado="MODIFICAR", 
            datos_presupuesto=seleccionado
        )
        if guardado:
            self.cargar()

    def eliminar(self):
        """Borra el presupuesto seleccionado tras confirmación."""
        seleccionado = self.tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un presupuesto para eliminar.", parent=self.ventana)
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Seguro que desea eliminar el presupuesto N° {seleccionado}?\nEsta acción no se puede deshacer.",
            parent=self.ventana
        )
        if not confirmar:
            return

        if self.modelo.eliminar_presupuesto(seleccionado):
            messagebox.showinfo("Éxito", "Presupuesto eliminado correctamente.", parent=self.ventana)
            self.cargar()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el registro.", parent=self.ventana)

    def imprimir(self):
        """Genera y abre el comprobante PDF del presupuesto seleccionado."""
        seleccionado = self.tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un presupuesto para imprimir.", parent=self.ventana)
            return

        id_presupuesto = int(seleccionado)

        # 1. Traer datos de la BD (cabecera y desgloses)
        cabecera = self.modelo.obtener_por_id(id_presupuesto)
        detalles = self.modelo.obtener_detalles_por_id(id_presupuesto)

        if not cabecera:
            messagebox.showerror("Error", "No se encontraron los datos del presupuesto en la base de datos.", parent=self.ventana)
            return

        try:
            # 2. Generar archivo PDF con el membrete de Tornería Gonzales
            ruta_pdf = generar_pdf_presupuesto(cabecera, detalles)

            # 3. Abrir el PDF de forma automática
            os.startfile(ruta_pdf)

        except Exception as e:
            messagebox.showerror("Error al generar PDF", f"No se pudo crear el archivo PDF:\n{e}", parent=self.ventana)