import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def execute_query(query, params=None, fetch=False):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            if fetch:
                return cur.fetchall()
            conn.commit()


def init_db():
    with open("database/schema.sql", "r") as f:
        sql = f.read()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
