import os
import sys

def obtener_ruta_base():
    """
    Determina la ruta del directorio donde se encuentra el script o el ejecutable.
    """
    if getattr(sys, 'frozen', False):
        # Si es un ejecutable (.exe)
        return os.path.dirname(sys.executable)
    else:
        # Si es un script .py
        return os.path.dirname(os.path.abspath(__file__))

def obtener_ruta_db():
    """
    Busca las bases de datos disponibles y retorna la primera que encuentre.
    Mantiene la prioridad definida en la lista.
    """
    base_path = obtener_ruta_base()
    
    # Definimos los nombres de las bases de datos de las dos plantas
    nombres_db = ["torneria.db"]
    
    for nombre in nombres_db:
        ruta_tentativa = os.path.join(base_path, nombre)
        if os.path.exists(ruta_tentativa):
            return ruta_tentativa
    
    # Si llega aquí, es porque no encontró ninguna de las dos
    # Podrías retornar None o lanzar un error para evitar que el programa falle silenciosamente
    return None

# Ejemplo de uso al conectar (suponiendo que usas sqlite3)
# ruta_db = obtener_ruta_db()
# if ruta_db:
#     conexion = sqlite3.connect(ruta_db)
# else:
#     print("Error: No se encontró ninguna base de datos en la carpeta del programa.")