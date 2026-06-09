from pathlib import Path
from sqlalchemy import text

from app import getSession

SQL_FILES = [
    "sql_scripts/tarea2.sql",
    "sql_scripts/region-comuna.sql",
    "sql_scripts/seed_data/01_populate_users.sql",
    "sql_scripts/seed_data/02_populate_actividades.sql",
]

session = getSession()
engine = session.get_bind()

# clean db
with engine.begin() as conn:
    conn.exec_driver_sql("SET FOREIGN_KEY_CHECKS = 0")
    tables = conn.exec_driver_sql("SHOW TABLES").fetchall()
    for (table_name,) in tables:
        conn.exec_driver_sql(f"DROP TABLE `{table_name}`")
    conn.exec_driver_sql("SET FOREIGN_KEY_CHECKS = 1")

# seed data
with engine.begin() as conn:
    for file_path in SQL_FILES:
        print(f"Cargando {file_path}")
        sql = Path(file_path).read_text(encoding="utf-8")
        # separamos por ; , al parecer no se puede llegar y ejecutar un .sql en con PySql
        statements = [stmt.strip() for stmt in sql.split(";") if stmt.strip()] 
        for stmt in statements:
            conn.execute(text(stmt))

session.close()

print("DB creada correctamente.")
