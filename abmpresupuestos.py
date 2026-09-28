# abmpresupuestos.py
from abmpresupuestoscontrolador import ABMPresupuestosControlador

def iniciar_presupuesto_abm(parent, conexion, estado="AGREGAR", datos_presupuesto=None):
    """
    Punto de entrada al formulario (ABM) de Presupuestos.
    Retorna True si se guardó con éxito para refrescar la grilla principal.
    """
    controlador = ABMPresupuestosControlador(parent, conexion, estado, datos_presupuesto)
    return controlador.guardado_exitoso