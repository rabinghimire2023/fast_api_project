import sqlite3

con = sqlite3.connect("app/data.db",check_same_thread=False)
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS Employees(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department TEXT NOT NULL
    );""")
con.commit()