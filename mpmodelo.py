class MateriasPrimasModelo:
    def __init__(self, conexion):
        self.conexion = conexion

    def _texto(self, v):
        return str(v).strip() if v else ""

    def _decimal(self, v):
        try:
            return float(v) if v is not None else 0.0
        except ValueError:
            return 0.0

    # -------------------------
    # OBTENER TODOS
    # -------------------------
    def obtener_todos(self):
        cur = self.conexion.cursor()
        # CORREGIDO: Se removió la coma extra después de precio_unitario
        cur.execute("""
            SELECT
                id_material,
                nombre,
                unidad_medida,
                precio_unitario
            FROM materias_primas
            ORDER BY id_material
        """)

        datos = []
        for fila in cur.fetchall():
            # CORREGIDO: Se quitó la variable 'stock' del desempaque
            id_, nombre, unidad, precio = fila
            datos.append({
                "id": id_,
                "nombre": self._texto(nombre),
                "unidad_medida": self._texto(unidad),
                "precio_unitario": self._decimal(precio),
            })

        cur.close()
        return datos

    # -------------------------
    # FILTRO
    # -------------------------
    def filtrar(self, campo, valor):
        registros = self.obtener_todos()
        if not campo or not valor:
            return registros

        campo = campo.lower().strip()
        valor = valor.strip().lower()
        resultado = []

        for r in registros:
            if campo == "id" and valor in str(r["id"]):
                resultado.append(r)
            elif campo == "nombre" and valor in r["nombre"].lower():
                resultado.append(r)
            elif campo == "u. medida" and valor in r["unidad_medida"].lower():
                resultado.append(r)
            elif campo == "precio" and valor in str(r["precio_unitario"]):
                resultado.append(r)
           
        return resultado

    # -------------------------
    # OBTENER POR ID
    # -------------------------
    def obtener_por_id(self, id_material):
        cur = self.conexion.cursor()
        # CORREGIDO: Se removió la coma extra después de precio_unitario
        cur.execute("""
            SELECT
                id_material,
                nombre,
                unidad_medida,
                precio_unitario
            FROM materias_primas
            WHERE id_material = ?
        """, (id_material,))

        fila = cur.fetchone()
        cur.close()

        if not fila:
            return None

        # CORREGIDO: Se quitó la variable 'stock' del desempaque
        id_, nombre, unidad, precio = fila
        return {
            "id_material": id_,
            "nombre": self._texto(nombre),
            "unidad_medida": self._texto(unidad),
            "precio_unitario": self._decimal(precio),
        }

    # -------------------------
    # ELIMINAR REGISTRO
    # -------------------------
    def eliminar_material(self, id_material):
        cursor = self.conexion.cursor()
        try:
            cursor.execute("DELETE FROM materias_primas WHERE id_material = ?", (id_material,))
            self.conexion.commit()
            return True
        except Exception as e:
            self.conexion.rollback()
            print("Error al eliminar materia prima:", e)
            return False
        finally:
            cursor.close()