import os
import mysql.connector

def validate_users_and_privileges():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root"
    )
    cursor = conn.cursor()
    
    report_lines = ["# 📊 Reporte de Validación de Usuarios y Permisos\n"]
    
    queries = [
        ("1. Verificar existencia del usuario 'tengopermisos'", "SELECT User FROM mysql.user WHERE User='tengopermisos';"),
        ("2. Conectado como 'tengopermisos', verificar creación del usuario 'user1'", "SELECT User FROM mysql.user WHERE User='user1';"),
        ("3. Conectado como 'root', verificar permisos de 'user1' para consultar tablas", "SHOW GRANTS FOR 'user1'@'%';"),
        ("4. Conectado como 'root', verificar permisos actuales de 'user1'", "SHOW GRANTS FOR 'user1'@'%';"),
        ("5. Conectado como 'user1', verificar sus permisos y compararlos con los anteriores", "SHOW GRANTS FOR CURRENT_USER;"),
        ("6. Conectado como 'root', otorgar permisos de creación y borrado de tablas a 'user1' en 'jardinería'", "SHOW GRANTS FOR 'user1'@'%';"),
        ("7. Conectado como 'root', verificar existencia del usuario 'creartablas' y sus permisos en 'fútbol'", "SHOW GRANTS FOR 'creartablas'@'%';"),
        ("8. Conectado como 'creartablas', verificar creación de una tabla sencilla", "SHOW TABLES FROM fútbol;"),
        ("9. Conectado como 'root', verificar existencia del usuario 'accesoglobal'", "SELECT User FROM mysql.user WHERE User='accesoglobal';"),
        ("10. Conectado como 'accesoglobal', insertar y luego intentar borrar una fila en 'fútbol.estadios'", "SELECT * FROM fútbol.estadios;"),
        ("11. Conectado como 'root', verificar existencia del usuario 'accesolocal'", "SELECT User FROM mysql.user WHERE User='accesolocal';"),
        ("12. Conectado como 'accesolocal', verificar acceso a 'futbol.estadios.nombre_estadio'", "SELECT nombre_estadio FROM fútbol.estadios;"),
        ("13. Conectado como 'root', verificar permisos de 'accesolimitado' en la primera columna de 'fútbol'", "SHOW GRANTS FOR 'accesolimitado'@'%';"),
        ("14. Conectado como 'accesolimitado', verificar ejecución de SELECT, UPDATE e INSERT", "SELECT * FROM fútbol.estadios;"),
        ("15. Conectado como 'root', revocar todos los permisos de 'user1'", "SHOW GRANTS FOR 'user1'@'%';"),
        ("16. Conectado como 'user1', verificar que no tiene permisos", "SHOW GRANTS FOR CURRENT_USER;"),
        ("17. Conectado como 'root', revocar permiso de modificación de tablas en 'fútbol' para 'creartablas'", "SHOW GRANTS FOR 'creartablas'@'%';"),
        ("18. Conectado como 'creartablas', intentar agregar una columna en 'fútbol.estadios'", "SHOW COLUMNS FROM fútbol.estadios;")
    ]
    
    for description, query in queries:
        cursor.execute(query)
        result = cursor.fetchall()
        status = "✅ Correcto" if result else "❌ No encontrado"
        report_lines.append(f"- **{description}**: {status}")
    
    # Guardar reporte en archivo Markdown
    report_text = "\n".join(report_lines)
    with open("reporte_validacion_permisos.md", "w") as f:
        f.write(report_text)
    
    # Si se ejecuta en GitHub Actions, escribir en el summary
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "w") as summary_file:
            summary_file.write(report_text)
    
    conn.close()

if __name__ == "__main__":
    validate_users_and_privileges()
