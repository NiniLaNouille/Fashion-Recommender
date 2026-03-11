from database.db import get_connection


def init_db():

    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS products(
        id TEXT PRIMARY KEY,
        title TEXT,
        brand TEXT,
        category TEXT,
        color TEXT,
        price REAL,
        description TEXT,
        image_url TEXT,
        product_url TEXT,
        source TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
        product_id TEXT,
        rating INTEGER
    )
    """)

    conn.commit()
