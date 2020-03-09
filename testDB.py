import sqlite3

DB_URL = r'db.sqlite3'

conn = sqlite3.connect(":memory:", check_same_thread = False)
cour = conn.cursor()

result = cour.execute("CREATE TABLE main_table(id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Surname VARCHAR(255), Number VARCHR(255), Card VARCHAR(255));")
print(result)