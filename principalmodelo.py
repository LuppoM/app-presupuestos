import sqlite3
import shutil
import os
from datetime import datetime
from seleccionbd import obtener_ruta_db

def obtener_conexion():
    """ 
    Establece la conexión con la base de datos única.
    Optimizado para red local (LAN) eliminando el modo WAL que suele dar lag.
    """
    db_path = obtener_ruta_db()
    
    # timeout=30 permite que si otro usuario está escribiendo, el programa espere
    conexion = sqlite3.connect(db_path, timeout=30)

    # Configuraciones de rendimiento para Red Local
    conexion.execute("PRAGMA journal_mode=DELETE;") # Más estable en redes LAN
    conexion.execute("PRAGMA synchronous=NORMAL;")
    conexion.execute("PRAGMA cache_size=-2000;") # Reserva 2MB de RAM para caché
    
    return conexion

def realizar_backup():
    """
    Crea una copia de seguridad de la base de datos actual.
    Mantiene un historial de los últimos 10 backups.
    """
    try:
        ruta_original = obtener_ruta_db()
        if not os.path.exists(ruta_original):
            return False, "No se encontró la base de datos original."

        # Crear carpeta de backups donde está la DB
        directorio_db = os.path.dirname(ruta_original)
        carpeta_backups = os.path.join(directorio_db, "Backups_Sistema")
        
        if not os.path.exists(carpeta_backups):
            os.makedirs(carpeta_backups)

        # Nombre con fecha y hora para no sobreescribir
        fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre_backup = f"TORNERIA_BAK_{fecha_hora}.db"
        ruta_destino = os.path.join(carpeta_backups, nombre_backup)

        # Copia física del archivo
        shutil.copy2(ruta_original, ruta_destino)
        
        # Limpieza de backups viejos (mantenemos 10)
        gestionar_limpieza_backups(carpeta_backups, 10)
        
        return True, ruta_destino
    except Exception as e:
        return False, str(e)

def gestionar_limpieza_backups(carpeta, limite):
    """ Borra los backups más antiguos si superan el límite """
    archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.endswith('.db')]
    archivos.sort(key=os.path.getmtime) # Los más viejos primero
    
    while len(archivos) > limite:
        archivo_viejo = archivos.pop(0)
        try:
            os.remove(archivo_viejo)
        except:
            pass