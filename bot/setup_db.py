import sqlite3

dbname = "./database.db"
conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute(
    "CREATE TABLE embed(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, content STRING)"
)
cur.execute(
    "CREATE TABLE var(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING, content STRING)"
)
conn.commit()
conn.close()
