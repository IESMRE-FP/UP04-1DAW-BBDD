import os
import mysql.connector

def validate_database():
    expected_tables = {
        "pais": {"id_pais", "nombre", "ultima_actualizacion","num_habitantes"},
        "ciudad": {"id_ciudad", "nombre", "ultima_actualizacion","id_pais","num_habitantes"},
        "direccion": {"id_direccion", "direccion", "direccion2", "distrito", "codigo_postal", "telefono", "ultima_actualizacion","id_ciudad"},
        "cliente": {"id_cliente", "nombre", "apellido1","apellido2", "email", "id_direccion", "activo", "fecha_creacion", "ultima_actualizacion"},
    }

    expected_primary_keys = {
        "pais": {"id_pais"},
        "ciudad": {"id_ciudad"},
        "direccion": {"id_direccion"},
        "cliente": {"id_cliente"},
    }

    expected_foreign_keys = {
        "cliente": {"id_direccion": "direccion"},
    }

    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="clientes"
    )
    cursor = conn.cursor()
    
    report_lines = ["# 📊 Reporte de Validación de Clientes\n"]
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


        # 2️⃣ Verificar relación ciudad - dirección
    report_lines.append("\n## 🔗 Verificación de Relación `ciudad` - `direccion`")
    cursor.execute("""
        SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_NAME = 'direccion' AND REFERENCED_TABLE_NAME = 'ciudad';
    """)
    relation_exists = cursor.fetchone()
    report_lines.append(f"- **Relación `id_ciudad`**: {'✅ Correcta' if relation_exists else '❌ Incorrecta'}")

    # 3️⃣ Verificar relación país - ciudad
    report_lines.append("\n## 🔗 Verificación de Relación `pais` - `ciudad`")
    cursor.execute("""
        SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_NAME = 'ciudad' AND REFERENCED_TABLE_NAME = 'pais';
    """)
    relation_exists = cursor.fetchone()
    report_lines.append(f"- **Relación `id_pais`**: {'✅ Correcta' if relation_exists else '❌ Incorrecta'}")

    # 4️⃣ Verificar cambio en `cliente` (apellidos -> apellido1 y apellido2)
    report_lines.append("\n## 🔄 Verificación de Cambio en `cliente`")
    cursor.execute("DESCRIBE cliente;")
    columns = {col[0] for col in cursor.fetchall()}
    
    apellido_status = "✅ Correcto" if "apellido1" in columns and "apellido2" in columns and "apellidos" not in columns else "❌ Incorrecto"
    report_lines.append(f"- **Cambio `apellidos → apellido1, apellido2`**: {apellido_status}")

    # 5️⃣ Verificar modificación de `distrito`
    report_lines.append("\n## 🏙️ Verificación de `distrito` en `direccion`")
    cursor.execute("SHOW COLUMNS FROM direccion LIKE 'distrito';")
    distrito_column = cursor.fetchone()
    distrito_status = "✅ Correcto" if distrito_column and distrito_column[1] == "varchar(50)" else "❌ Incorrecto"
    report_lines.append(f"- **`distrito` ahora `VARCHAR(50)`**: {distrito_status}")

    # 6️⃣ Verificar `num_habitantes` en `ciudad` y `pais`
    report_lines.append("\n## 👥 Verificación de `num_habitantes` en `ciudad` y `pais`")
    cursor.execute("SHOW COLUMNS FROM ciudad LIKE 'num_habitantes';")
    ciudad_status = "✅ Correcto" if cursor.fetchone() else "❌ Incorrecto"

    cursor.execute("SHOW COLUMNS FROM pais LIKE 'num_habitantes';")
    pais_status = "✅ Correcto" if cursor.fetchone() else "❌ Incorrecto"

    report_lines.append(f"- **`num_habitantes` en `ciudad`**: {ciudad_status}")
    report_lines.append(f"- **`num_habitantes` en `pais`**: {pais_status}")

    # 7️⃣ Verificar cambio de `telefono` a `INT`
    report_lines.append("\n## 📞 Verificación de `telefono` en `direccion`")
    cursor.execute("SHOW COLUMNS FROM direccion LIKE 'telefono';")
    telefono_column = cursor.fetchone()
    telefono_status = "✅ Correcto" if telefono_column and "int" in telefono_column[1] else "❌ Incorrecto"
    report_lines.append(f"- **`telefono` ahora `INT`**: {telefono_status}")

    # Guardar reporte en archivo Markdown
    report_text = "\n".join(report_lines)
    with open("reporte_validacion_clientes.md", "w") as f:
        f.write(report_text)

    # Si se ejecuta en GitHub Actions, escribir en el summary
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "w") as summary_file:
            summary_file.write(report_text)

    conn.close()

if __name__ == "__main__":
    validate_database()
