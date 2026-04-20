import sqlite3

conn = sqlite3.connect("etf_monitor.db")
cursor = conn.cursor()


# CHECK 1: Find any days where an ETF has no price data
def check_missing_prices():
    cursor.execute("""
        SELECT ticker, COUNT(*) as total_days
        FROM daily_prices
        GROUP BY ticker
    """)
    results = cursor.fetchall()
    for row in results:
        ticker = row[0]
        days = row[1]
        print(f"{ticker} has {days} days of data")
        if days < 60:
            cursor.execute("""
                INSERT INTO alerts (type, message, date)
                VALUES (?, ?, date('now'))
            """, ("missing_data", f"{ticker} only has {days} days of data, expected ~62"))
            print(f"  ALERT: {ticker} might have missing days!")


# CHECK 2: Find any day where the price jumped more than 10%
def check_big_price_jumps():
    cursor.execute("""
        SELECT ticker, date, open, close
        FROM daily_prices
    """)
    results = cursor.fetchall()
    for row in results:
        ticker = row[0]
        date = row[1]
        open_price = row[2]
        close_price = row[3]
        if open_price > 0:
            change = abs(close_price - open_price) / open_price * 100
            if change > 10:
                cursor.execute("""
                    INSERT INTO alerts (type, message, date)
                    VALUES (?, ?, ?)
                """, ("big_jump", f"{ticker} moved {change:.1f}% on {date}", date))
                print(f"  ALERT: {ticker} moved {change:.1f}% on {date}")


# CHECK 3: Find any day where volume is unusually low
def check_low_volume():
    tickers = ["SPY", "QQQ", "IVV", "AGG", "GLD"]
    for ticker in tickers:
        cursor.execute("""
            SELECT AVG(volume) FROM daily_prices
            WHERE ticker = ?
        """, (ticker,))
        avg_volume = cursor.fetchone()[0]

        cursor.execute("""
            SELECT date, volume FROM daily_prices
            WHERE ticker = ? AND volume < ?
        """, (ticker, avg_volume * 0.3))
        results = cursor.fetchall()

        for row in results:
            date = row[0]
            volume = row[1]
            cursor.execute("""
                INSERT INTO alerts (type, message, date)
                VALUES (?, ?, ?)
            """, ("low_volume", f"{ticker} volume was {volume} on {date}, avg is {avg_volume:.0f}", date))
            print(f"  ALERT: {ticker} had low volume on {date}")


# CHECK 4: Find duplicate records
def check_duplicates():
    cursor.execute("""
        SELECT ticker, date, COUNT(*)
        FROM daily_prices
        GROUP BY ticker, date
        HAVING COUNT(*) > 1
    """)
    results = cursor.fetchall()
    for row in results:
        ticker = row[0]
        date = row[1]
        count = row[2]
        cursor.execute("""
            INSERT INTO alerts (type, message, date)
            VALUES (?, ?, ?)
        """, ("duplicate", f"{ticker} has {count} entries for {date}", date))
        print(f"  ALERT: {ticker} has {count} duplicate entries on {date}")


# Run all checks
print("Running data quality checks...\n")

print("Check 1: Missing prices")
check_missing_prices()

print("\nCheck 2: Big price jumps (>10%)")
check_big_price_jumps()

print("\nCheck 3: Low volume days")
check_low_volume()

print("\nCheck 4: Duplicate records")
check_duplicates()

conn.commit()
conn.close()

print("\nAll checks complete! Results saved to alerts table.")