import sqlite3

conn = sqlite3.connect("devises.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        name TEXT PRIMARY KEY,
        last_seen TEXT,
        status TEXT
    )
""")
conn.commit()
conn.close()
