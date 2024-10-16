"""
initial-migration
"""

from yoyo import step

__depends__ = {}

def create_base_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tags(
    id SERIAL PRIMARY KEY UNIQUE NOT NULL,
    muid UUID NOT NULL,
    quality VARCHAR NOT NULL);""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS measurement(
    id SERIAL PRIMARY KEY UNIQUE NOT NULL,
    measurement VARCHAR NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    energy DOUBLE PRECISION NOT NULL,
    tags_id INTEGER NOT NULL REFERENCES tags (id));""")


def rollback_base_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
    DROP TABLE IF EXISTS measurement;""")

    cursor.execute("""
    DROP TABLE IF EXISTS tags;""")


steps = [
    step(create_base_tables, rollback_base_tables)
]
