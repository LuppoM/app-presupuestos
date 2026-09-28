from tkinter import messagebox
from mpmodelo import MateriasPrimasModelo
from mpvista import (
    crear_ventana,
    crear_toolstrip,
    crear_filtro,
    crear_tabla
)

# Importación directa de tu formulario ABM
from mpabm import iniciar_mpabm

class MateriasPrimasControlador:
    def __init__(self, parent, conexion):
        self.parent = parent
        self.modelo = MateriasPrimasModelo(conexion)
        self.ventana = crear_ventana(parent)

        # Barra de Herramientas
        crear_toolstrip(
            self.ventana,
            abrir_agregar=self.agregar,
            abrir_modificar=self.modificar,
            abrir_eliminar=self.eliminar
        )

        # Filtro de Búsqueda
        self.combo, self.entry = crear_filtro(self.ventana, self.aplicar_filtro)

        # Rejilla de Datos (Tabla)
        self.tree = crear_tabla(self.ventana)

        # Carga Inicial de Datos
        self.cargar()

    def cargar(self, filas=None):
        self.tree.delete(*self.tree.get_children())
        datos = filas if filas is not None else self.modelo.obtener_todos()

        for d in datos:
            self.tree.insert(
                "",
                "end",
                iid=d["id"],
                values=(
                    d["id"],
                    d["nombre"],
                    d["unidad_medida"],
                    f"$ {d['precio_unitario']:.2f}",
                )
            )

    def aplicar_filtro(self, campo, valor):
        filas = self.modelo.filtrar(campo, valor)
        self.cargar(filas)

    # =====================================================
    # AGREGAR MATERIAL
    # =====================================================
    def agregar(self):
        # Llamamos directamente a iniciar_mpabm en modo AGREGAR
        guardado = iniciar_mpabm(
            parent=self.ventana,
            conexion=self.modelo.conexion,
            estado="AGREGAR"
        )
        # Si el formulario retornó True (guardado exitoso), refrescamos la tabla
        if guardado:
            self.cargar()

    # =====================================================
    # MODIFICAR MATERIAL
    # =====================================================
    def modificar(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un material para modificar", parent=self.ventana)
            return

        datos_material = self.modelo.obtener_por_id(seleccionado)
        
        # Pasamos los datos recuperados a iniciar_mpabm en modo MODIFICAR
        guardado = iniciar_mpabm(
            parent=self.ventana,
            conexion=self.modelo.conexion,
            estado="MODIFICAR",
            datos_mp=datos_material
        )
        # Si se confirmaron los cambios en el formulario, refrescamos la tabla
        if guardado:
            self.cargar()

    # =====================================================
    # ELIMINAR DIRECTO (SIN CONTRASEÑA)
    # =====================================================
    def eliminar(self):
        seleccionado = self.tree.focus()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione un material para eliminar", parent=self.ventana)
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación", 
            f"¿Seguro que desea eliminar el material ID {seleccionado} de la lista?",
            parent=self.ventana
        )

        if not confirmar:
            return

        if self.modelo.eliminar_material(seleccionado):
            messagebox.showinfo("Éxito", "Materia prima eliminada correctamente", parent=self.ventana)
            self.cargar()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el elemento seleccionado", parent=self.ventana)