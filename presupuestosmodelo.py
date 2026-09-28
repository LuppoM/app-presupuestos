class PresupuestosModelo:
    def __init__(self, conexion):
        self.conexion = conexion

    def _obtener_nombre_tabla_detalles(self, cursor):
        """Busca en la base de datos cuál es la tabla real de detalles usada."""
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = [fila[0] for fila in cursor.fetchall()]
        
        # Lista de nombres posibles para la tabla de detalles
        posibles_nombres = ["presupuesto_detalles", "presupuestos_detalle", "presupuesto_detalle", "detalles_presupuesto"]
        
        for nombre in posibles_nombres:
            if nombre in tablas:
                return nombre
                
        # Si no encuentra ninguna conocida, busca alguna que contenga 'detalle'
        for t in tablas:
            if "detalle" in t.lower():
                return t
                
        return None

    def obtener_todos(self):
        """Trae los presupuestos para la grilla principal."""
        cur = self.conexion.cursor()
        cur.execute("""
            SELECT id_presupuesto, fecha, cliente, descripcion, total_general 
            FROM presupuestos 
            ORDER BY id_presupuesto DESC
        """)
        
        datos = []
        for fila in cur.fetchall():
            id_, fecha, cliente, desc, total_gen = fila
            datos.append({
                "id": id_,
                "fecha": str(fecha).strip() if fecha else "",
                "cliente": str(cliente).strip() if cliente else "",
                "descripcion": str(desc).strip() if desc else "",
                "total_general": float(total_gen) if total_gen else 0.0
            })
        cur.close()
        return datos

    def obtener_por_id(self, id_presupuesto):
        """Obtiene la cabecera de un presupuesto."""
        cur = self.conexion.cursor()
        cur.execute("""
            SELECT id_presupuesto, fecha, cliente, descripcion, mano_obra, total_general
            FROM presupuestos
            WHERE id_presupuesto = ?
        """, (id_presupuesto,))
        fila = cur.fetchone()
        cur.close()
        
        if fila:
            id_, fecha, cliente, desc, mo, total_gen = fila
            mo_val = float(mo) if mo else 0.0
            total_gen_val = float(total_gen) if total_gen else 0.0
            
            return {
                "id": id_,
                "id_presupuesto": id_,
                "fecha": str(fecha).strip() if fecha else "",
                "cliente": str(cliente).strip() if cliente else "",
                "descripcion": str(desc).strip() if desc else "",
                "mano_obra": mo_val,
                "total_materiales": round(total_gen_val - mo_val, 2),
                "total_general": total_gen_val
            }
        return None

    def obtener_detalles_por_id(self, id_presupuesto):
        """
        Obtiene los detalles vinculando presupuesto_detalles con materias_primas.
        """
        cur = self.conexion.cursor()
        
        # Consulta SQL haciendo JOIN con la tabla materias_primas
        query = """
            SELECT 
                m.nombre, 
                d.cantidad, 
                m.unidad_medida, 
                d.precio_venta, 
                (d.cantidad * d.precio_venta) AS subtotal
            FROM presupuesto_detalles d
            JOIN materias_primas m ON d.id_material = m.id_material
            WHERE d.id_presupuesto = ?
        """
        
        detalles = []
        try:
            cur.execute(query, (id_presupuesto,))
            filas = cur.fetchall()
            
            for fila in filas:
                nombre, cantidad, unidad, precio_venta, subtotal = fila
                
                detalles.append({
                    "nombre": nombre,
                    "cantidad": cantidad,
                    "unidad": unidad if unidad else "",
                    "precio_venta": float(precio_venta),
                    "subtotal": float(subtotal)
                })
        except Exception as e:
            print(f"Error al obtener detalles del presupuesto #{id_presupuesto}: {e}")
            
        cur.close()
        return detalles

    def eliminar_presupuesto(self, id_presupuesto):
        """Borra la cabecera y sus detalles detectando automáticamente la tabla."""
        cursor = self.conexion.cursor()
        try:
            tabla_detalles = self._obtener_nombre_tabla_detalles(cursor)
            if tabla_detalles:
                cursor.execute(f"DELETE FROM {tabla_detalles} WHERE id_presupuesto = ?", (id_presupuesto,))

            cursor.execute("DELETE FROM presupuestos WHERE id_presupuesto = ?", (id_presupuesto,))
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            print("Error al eliminar presupuesto en modelo:", e)
            return False
        finally:
            cursor.close()