import os
import psycopg2
import sqlite3
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG

USE_SQLITE = os.getenv("USE_SQLITE", "true").lower() == "true"

def get_connection():
    if USE_SQLITE:
        conn = sqlite3.connect("fanikio.db")
        conn.row_factory = sqlite3.Row
        return conn
    return psycopg2.connect(**DB_CONFIG)


def execute_query(query, params=None, fetch=False):
    # Adapt query for SQLite
    if USE_SQLITE:
        if params:
            query = query.replace("%s", "?")
        query = query.replace("NOW()", "CURRENT_TIMESTAMP")
    
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, params or ())
        if fetch:
            rows = cur.fetchall()
            if USE_SQLITE:
                # Convert sqlite3.Row to dict to match RealDictCursor behavior
                return [dict(row) for row in rows]
            return rows
        conn.commit()


def init_db():
    if USE_SQLITE:
        print("Initializing SQLite database...")
        with open("database/schema.sql", "r") as f:
            sql = f.read()
        # Remove PostgreSQL specific commands or adapt them
        sql = sql.replace("SERIAL PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
        sql = sql.replace("NUMERIC(4,2)", "REAL")
        sql = sql.replace("NOW()", "CURRENT_TIMESTAMP")
        sql = sql.replace("TIMESTAMP", "DATETIME")
        
        # Split sql by semicolon to execute one by one in sqlite
        with get_connection() as conn:
            for statement in sql.split(";"):
                if statement.strip():
                    conn.execute(statement)
        print("SQLite database initialized successfully.")
    else:
        with open("database/schema.sql", "r") as f:
            sql = f.read()
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
            conn.commit()
        print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
