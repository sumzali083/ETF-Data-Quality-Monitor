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

cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_prices (
        id INTEGER PRIMARY KEY,
        ticker TEXT NOT NULL,
        date TEXT NOT NULL,
        open REAL,
        close REAL,
        high REAL,
        low REAL,
        volume INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY,
        type TEXT NOT NULL,
        message TEXT,
        date TEXT NOT NULL
    )
""")
conn.commit()
conn.close()

print("Database created!")