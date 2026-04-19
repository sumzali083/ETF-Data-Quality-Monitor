import sqlite3

conn = sqlite3.connect("etf_monitor.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS etfs (
        id INTEGER PRIMARY KEY,
        ticker TEXT NOT NULL,
        name TEXT
    )
""")

conn.commit()
conn.close()

print("Database created!")