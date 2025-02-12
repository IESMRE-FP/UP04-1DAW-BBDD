import os
import mysql.connector

def validate_database():
    expected_tables = {
        "actor": {"id_actor", "nombre", "apellidos", "ultima_actualizacion"},
        "categoria": {"id_categoria", "nombre", "ultima_actualizacion"},
        "idioma": {"id_idioma", "nombre", "ultima_actualizacion"},
        "pelicula": {"id_pelicula", "titulo", "descripcion", "anyo_lanzamiento", "id_idioma", "id_idioma_original", "duracion_alquiler", "rental_rate", "duracion", "replacement_cost", "clasificacion", "caracteristicas_especiales", "ultima_actualizacion"},
        "pelicula_categoria": {"id_pelicula", "id_categoria", "ultima_actualizacion"},
        "inventario": {"id_inventario", "ultima_actualizacion"},
    }

    expected_primary_keys = {
        "actor": {"id_actor"},
        "categoria": {"id_categoria"},
        "idioma": {"id_idioma"},
        "pelicula": {"id_pelicula"},
        "pelicula_categoria": {"id_pelicula", "id_categoria"},
        "inventario": {"id_inventario"},
    }

    expected_foreign_keys = {
        "pelicula": {"id_idioma": "idioma", "id_idioma_original": "idioma"},
        "pelicula_categoria": {"id_pelicula": "pelicula", "id_categoria": "categoria"},
    }

    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="peliculas"
    )
    cursor = conn.cursor()
    
    report_lines = ["# 📊 Reporte de Validación de Películas\n"]
    # Pregunta 1: Verificar que las tablas fueron creadas
    report_lines.append("\n## 1️⃣ Verificación de Creación de Tablas")

    # Verificar tablas
    cursor.execute("SHOW TABLES;")
    found_tables = {table[0] for table in cursor.fetchall()}
    report_lines.append("## 📌 Verificación de Tablas")
    for table in expected_tables.keys():
        status = "✅ Correcta" if table in found_tables else "❌ Faltante"
        report_lines.append(f"- **{table}**: {status}")
    
    # Verificar columnas
    report_lines.append("\n## 🏷️ Verificación de Columnas")
    for table, expected_columns in expected_tables.items():
        cursor.execute(f"DESCRIBE `{table}`;")
        found_columns = {col[0] for col in cursor.fetchall()}
        status = "✅ Correctas" if found_columns == expected_columns else "❌ Incorrectas"
        report_lines.append(f"- **{table}**: {status}")
    
    # Verificar claves primarias
    report_lines.append("\n## 🔑 Verificación de Claves Primarias")
    for table, expected_pk in expected_primary_keys.items():
        cursor.execute(f"SHOW KEYS FROM `{table}` WHERE Key_name = 'PRIMARY';")
        found_pk = {row[4] for row in cursor.fetchall()}
        status = "✅ Correcta" if found_pk == expected_pk else "❌ Incorrecta"
        report_lines.append(f"- **{table}**: {status}")
    
    # Verificar claves foráneas
    report_lines.append("\n## 🔗 Verificación de Claves Foráneas")
    for table, expected_fks in expected_foreign_keys.items():
        cursor.execute(f"SELECT COLUMN_NAME, REFERENCED_TABLE_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_NAME = '{table}' AND REFERENCED_TABLE_NAME IS NOT NULL;")
        found_fks = {row[0]: row[1] for row in cursor.fetchall()}
        status = "✅ Correctas" if found_fks == expected_fks else "❌ Incorrectas"
        report_lines.append(f"- **{table}**: {status}")
    
    # Guardar reporte en archivo Markdown
    #report_text = "\n".join(report_lines)
    #with open("reporte_validacion.md", "w") as f:
        #f.write(report_text)

    # Pregunta 1: Verificar que las tablas fueron creadas
    report_lines.append("\n## 1️⃣ Verificación de Creación de Tablas")
    expected_tables = {"actor", "categoria", "idioma", "pelicula", "pelicula_categoria", "inventario"}
    cursor.execute("SHOW TABLES;")
    found_tables = {table[0] for table in cursor.fetchall()}
    status = "✅ Correcto" if expected_tables.issubset(found_tables) else "❌ Incompleto"
    report_lines.append(f"- **Creación de tablas**: {status}")

    # Pregunta 2: Verificar la inclusión de la columna 'edad' en actor
    report_lines.append("\n## 2️⃣ Inclusión de la columna 'edad' en 'actor'")
    cursor.execute("SHOW COLUMNS FROM actor LIKE 'edad';")
    result = cursor.fetchone()
    status = "✅ Correcto" if result and result[1] == "int" and result[2] == "NO" else "❌ Incorrecto"
    report_lines.append(f"- **Columna 'edad'**: {status}")

    # Pregunta 3: Verificar eliminación de 'apellidos' y creación de 'apellido1' y 'apellido2'
    report_lines.append("\n## 3️⃣ Modificación de columnas en 'actor'")
    cursor.execute("SHOW COLUMNS FROM actor LIKE 'apellidos';")
    result = cursor.fetchone()
    apellidos_status = "✅ Eliminada" if not result else "❌ Aún existe"
    
    cursor.execute("SHOW COLUMNS FROM actor LIKE 'apellido1';")
    result1 = cursor.fetchone()
    apellido1_status = "✅ Correcto" if result1 and result1[1] == "varchar(45)" and result1[2] == "NO" else "❌ Incorrecto"

    cursor.execute("SHOW COLUMNS FROM actor LIKE 'apellido2';")
    result2 = cursor.fetchone()
    apellido2_status = "✅ Correcto" if result2 and result2[1] == "varchar(45)" and result2[2] == "NO" else "❌ Incorrecto"

    report_lines.append(f"- **Columna 'apellidos' eliminada**: {apellidos_status}")
    report_lines.append(f"- **Columna 'apellido1' creada**: {apellido1_status}")
    report_lines.append(f"- **Columna 'apellido2' creada**: {apellido2_status}")

    # Pregunta 4: Verificar inclusión de la columna 'id_pelicula' en inventario
    report_lines.append("\n## 4️⃣ Relación entre 'inventario' y 'pelicula'")
    cursor.execute("SHOW COLUMNS FROM inventario LIKE 'id_pelicula';")
    result = cursor.fetchone()
    status = "✅ Correcto" if result and result[1] == "smallint(5) unsigned" and result[2] == "NO" else "❌ Incorrecto"
    report_lines.append(f"- **Columna 'id_pelicula' añadida**: {status}")

    # Pregunta 5: Verificar creación de 'pelicula_actor'
    report_lines.append("\n## 5️⃣ Creación de 'pelicula_actor'")
    cursor.execute("SHOW TABLES LIKE 'pelicula_actor';")
    result = cursor.fetchone()
    status = "✅ Correcto" if result else "❌ Faltante"
    report_lines.append(f"- **Tabla 'pelicula_actor'**: {status}")

    # Pregunta 6: Verificar modificación de 'nombre' en 'categoria'
    report_lines.append("\n## 6️⃣ Modificación de 'nombre' en 'categoria'")
    cursor.execute("SHOW COLUMNS FROM categoria LIKE 'nombre';")
    result = cursor.fetchone()
    status = "✅ Correcto" if result and result[1] == "varchar(50)" else "❌ Incorrecto"
    report_lines.append(f"- **Cambio a VARCHAR(50)**: {status}")

    # Pregunta 7: Verificar modificación de 'duracion_alquiler' en 'pelicula'
    report_lines.append("\n## 7️⃣ Modificación de 'duracion_alquiler' en 'pelicula'")
    cursor.execute("SHOW COLUMNS FROM pelicula LIKE 'duracion_alquiler';")
    result = cursor.fetchone()
    status = "✅ Correcto" if result and result[1] == "int(11)" and result[4] == "3" else "❌ Incorrecto"
    report_lines.append(f"- **Cambio a INT con valor por defecto 3**: {status}")

    # Pregunta 8: Verificar modificación de 'clasificacion' en 'pelicula'
    report_lines.append("\n## 8️⃣ Modificación de 'clasificacion' en 'pelicula'")
    cursor.execute("SHOW COLUMNS FROM pelicula LIKE 'clasificacion';")
    result = cursor.fetchone()
    status = "✅ Correcto" if result and "enum('G','PG','PG-13','R','NC-17')" in result[1] else "❌ Incorrecto"
    report_lines.append(f"- **Cambio a ENUM**: {status}")

    # Pregunta 9: Verificar modificación de 'caracteristicas_especiales' en 'pelicula'
    report_lines.append("\n## 9️⃣ Modificación de 'caracteristicas_especiales' en 'pelicula'")
    cursor.execute("SHOW COLUMNS FROM pelicula LIKE 'caracteristicas_especiales';")
    result = cursor.fetchone()
    status = "✅ Correcto" if result and "set('Trailers','Commentaries','Deleted Scenes','Behind the Scenes')" in result[1] else "❌ Incorrecto"
    report_lines.append(f"- **Cambio a SET**: {status}")

    # Guardar reporte en archivo Markdown
    report_text = "\n".join(report_lines)
    with open("reporte_validacion.md", "w") as f:
        f.write(report_text)

    print("\n".join(report_lines))

    # Si se ejecuta en GitHub Actions, escribir en el summary
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "w") as summary_file:
            summary_file.write(report_text)

    conn.close()

if __name__ == "__main__":
    validate_database()
