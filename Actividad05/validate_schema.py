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
    report_text = "\n".join(report_lines)
    with open("reporte_validacion.md", "w") as f:
        f.write(report_text)

    # Si se ejecuta en GitHub Actions, escribir en el summary
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "w") as summary_file:
            summary_file.write(report_text)

    conn.close()

if __name__ == "__main__":
    validate_database()
