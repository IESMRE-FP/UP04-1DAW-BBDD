import os
import mysql.connector

def validate_database():
    expected_tables = {
        "departamento": {"id", "nombre"},
        "persona": {"id", "nif", "nombre", "apellido1", "apellido2", "ciudad", "direccion", "telefono", "fecha_nacimiento", "sexo", "tipo"},
        "profesor": {"id_profesor", "id_departamento"},
        "grado": {"id", "nombre"},
        "asignatura": {"id", "nombre", "creditos", "tipo", "curso", "cuatrimestre", "id_profesor", "id_grado"},
        "curso_escolar": {"id", "anyo_inicio", "anyo_fin"},
        "alumno_se_matricula_asignatura": {"id_alumno", "id_asignatura", "id_curso_escolar"}
    }

    expected_primary_keys = {
        "departamento": {"id"},
        "persona": {"id"},
        "profesor": {"id_profesor"},
        "grado": {"id"},
        "asignatura": {"id"},
        "curso_escolar": {"id"},
        "alumno_se_matricula_asignatura": {"id_alumno", "id_asignatura", "id_curso_escolar"}
    }

    expected_foreign_keys = {
        "profesor": {"id_profesor": "persona", "id_departamento": "departamento"},
        "asignatura": {"id_profesor": "profesor", "id_grado": "grado"},
        "alumno_se_matricula_asignatura": {"id_alumno": "persona", "id_asignatura": "asignatura", "id_curso_escolar": "curso_escolar"}
    }

    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="universidad"
    )
    cursor = conn.cursor()
    
    report_lines = ["# 📊 Reporte de Validación de Universidad\n"]

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
    with open("reporte_validacion_universidad.md", "w") as f:
        f.write(report_text)

    # Si se ejecuta en GitHub Actions, escribir en el summary
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "w") as summary_file:
            summary_file.write(report_text)

    conn.close()

if __name__ == "__main__":
    validate_database()
