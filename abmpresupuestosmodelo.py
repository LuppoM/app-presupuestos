# abmpresupuestosmodelo.py

class ABMPresupuestosModelo:
    def __init__(self, conexion):
        self.conexion = conexion

    def obtener_materias_primas(self):
        """Trae los materiales disponibles en el catálogo para agregarlos al presupuesto"""
        cur = self.conexion.cursor()
        cur.execute("SELECT id_material, nombre, unidad_medida, precio_unitario FROM materias_primas ORDER BY nombre")
        materiales = []
        for fila in cur.fetchall():
            id_, nombre, unidad, precio = fila
            materiales.append({
                "id_material": id_,
                "nombre": str(nombre),
                "unidad_medida": str(unidad),
                "precio_unitario": float(precio)
            })
        cur.close()
        return materiales

    def obtener_por_id(self, id_presupuesto):
        """Trae la cabecera de un presupuesto por su ID"""
        cur = self.conexion.cursor()
        cur.execute("""
            SELECT id_presupuesto, fecha, cliente, descripcion, mano_obra, total_materiales, total_general
            FROM presupuestos 
            WHERE id_presupuesto = ?
        """, (id_presupuesto,))
        fila = cur.fetchone()
        cur.close()
        if fila:
            return {
                "id_presupuesto": fila[0],
                "fecha": fila[1],
                "cliente": fila[2],
                "descripcion": fila[3],
                "mano_obra": float(fila[4] or 0),
                "total_materiales": float(fila[5] or 0),
                "total_general": float(fila[6] or 0)
            }
        return None

    def obtener_detalles_por_id(self, id_presupuesto):
        """Trae las líneas de materiales asociadas al presupuesto"""
        cur = self.conexion.cursor()
        cur.execute("""
            SELECT pd.id_material, mp.nombre, mp.unidad_medida, pd.cantidad, pd.precio_venta
            FROM presupuesto_detalles pd
            INNER JOIN materias_primas mp ON pd.id_material = mp.id_material
            WHERE pd.id_presupuesto = ?
        """, (id_presupuesto,))
        detalles = []
        for fila in cur.fetchall():
            id_mat, nombre, unidad, cantidad, precio = fila
            detalles.append({
                "id_material": id_mat,
                "nombre": str(nombre),
                "unidad": str(unidad),
                "precio_venta": float(precio),
                "cantidad": float(cantidad),
                "subtotal": float(cantidad) * float(precio)
            })
        cur.close()
        return detalles

    def guardar_presupuesto(self, datos_cabecera, lista_detalles):
        """Inserta la cabecera y el desglose de materiales dentro de una transacción única"""
        cursor = self.conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO presupuestos (fecha, cliente, descripcion, mano_obra, total_materiales, total_general)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                datos_cabecera["fecha"],
                datos_cabecera["cliente"],
                datos_cabecera["descripcion"],
                datos_cabecera["mano_obra"],
                datos_cabecera["total_materiales"],
                datos_cabecera["total_general"]
            ))
            
            id_presupuesto = cursor.lastrowid

            for item in lista_detalles:
                cursor.execute("""
                    INSERT INTO presupuesto_detalles (id_presupuesto, id_material, cantidad, precio_venta)
                    VALUES (?, ?, ?, ?)
                """, (id_presupuesto, item["id_material"], item["cantidad"], item["precio_venta"]))

            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            print("Error al guardar presupuesto en transacción:", e)
            return False
        finally:
            cursor.close()

    def actualizar_presupuesto(self, id_presupuesto, datos_cabecera, lista_detalles):
        """Actualiza la cabecera y reemplaza sus detalles"""
        cursor = self.conexion.cursor()
        try:
            # 1. Actualizar la cabecera
            cursor.execute("""
                UPDATE presupuestos
                SET fecha = ?, cliente = ?, descripcion = ?, mano_obra = ?, total_materiales = ?, total_general = ?
                WHERE id_presupuesto = ?
            """, (
                datos_cabecera["fecha"],
                datos_cabecera["cliente"],
                datos_cabecera["descripcion"],
                datos_cabecera["mano_obra"],
                datos_cabecera["total_materiales"],
                datos_cabecera["total_general"],
                id_presupuesto
            ))

            # 2. Eliminar detalles anteriores y volver a insertarlos
            cursor.execute("DELETE FROM presupuesto_detalles WHERE id_presupuesto = ?", (id_presupuesto,))

            for item in lista_detalles:
                cursor.execute("""
                    INSERT INTO presupuesto_detalles (id_presupuesto, id_material, cantidad, precio_venta)
                    VALUES (?, ?, ?, ?)
                """, (id_presupuesto, item["id_material"], item["cantidad"], item["precio_venta"]))

            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            print("Error al actualizar presupuesto:", e)
            return False
        finally:
            cursor.close()