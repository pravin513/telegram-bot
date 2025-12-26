import sqlite3

def connect():
    return sqlite3.connect("products.db")

def init_db():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        keywords TEXT,
        price TEXT,
        link TEXT,
        photo TEXT,
        searches INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()

def add_product(name, keywords, price, link, photo):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, keywords, price, link, photo) VALUES (?, ?, ?, ?, ?)",
        (name, keywords, price, link, photo)
    )
    conn.commit()
    conn.close()

def search_products(text):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, price, link, photo FROM products WHERE keywords LIKE ?",
        (f"%{text}%",)
    )
    rows = cur.fetchall()

    for r in rows:
        cur.execute(
            "UPDATE products SET searches = searches + 1 WHERE id=?",
            (r[0],)
        )

    conn.commit()
    conn.close()
    return rows

def top_products(limit=5):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT name, searches FROM products ORDER BY searches DESC LIMIT ?",
        (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows
