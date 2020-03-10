import sqlite3

DB_URL = r'db.sqlite3'

#conn = sqlite3.connect(":memory:", check_same_thread = False)
conn = sqlite3.connect(DB_URL)

cour = conn.cursor()

result = cour.execute("SELECT * FROM main_table")
print(result.fetchall())