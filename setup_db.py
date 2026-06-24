import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_db():
    conn = psycopg2.connect("postgresql://postgres:postgres@localhost:5432/postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'emanagement'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("CREATE DATABASE emanagement")
        print("Database emanagement created successfully.")
    else:
        print("Database emanagement already exists.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_db()
