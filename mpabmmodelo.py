def insertar_materia_prima(conexion, datos):
    # Asegura que las claves coincidan exactamente con las columnas de la bd
    campos = ", ".join([f"[{k}]" for k in datos.keys()])
    placeholders = ", ".join(["?"] * len(datos))
    sql = f"INSERT INTO materias_primas ({campos}) VALUES ({placeholders})"

    cursor = conexion.cursor()
    cursor.execute(sql, list(datos.values()))
    conexion.commit()
    cursor.close()

def actualizar_materia_prima(conexion, id_material, datos):
    sets = ", ".join([f"[{k}] = ?" for k in datos.keys()])
    sql = f"UPDATE materias_primas SET {sets} WHERE id_material = ?"

    cursor = conexion.cursor()
    cursor.execute(sql, list(datos.values()) + [id_material])
    conexion.commit()
    cursor.close()

def obtener_proximo_id(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT MAX(id_material) FROM materias_primas")
    ultimo = cursor.fetchone()[0]
    cursor.close()

    return 1 if ultimo is None else ultimo + 1