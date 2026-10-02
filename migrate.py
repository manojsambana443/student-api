import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


load_dotenv()

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def get_db_connection():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


def run_migrations():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version VARCHAR(255) PRIMARY KEY,
                    applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

            migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))

            for migration_file in migration_files:
                version = migration_file.name

                cursor.execute(
                    "SELECT 1 FROM schema_migrations WHERE version = %s",
                    (version,)
                )

                if cursor.fetchone():
                    print(f"Already applied: {version}")
                    continue

                migration_sql = migration_file.read_text()

                cursor.execute(migration_sql)

                cursor.execute(
                    "INSERT INTO schema_migrations (version) VALUES (%s)",
                    (version,)
                )

                print(f"Applied: {version}")


if __name__ == "__main__":
    run_migrations()
