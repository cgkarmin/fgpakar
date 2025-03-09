import sqlite3

db_path = "database.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE karangan ADD COLUMN nama TEXT;")
    cursor.execute("ALTER TABLE karangan ADD COLUMN kelas TEXT;")
    conn.commit()
    print("✅ Lajur 'nama' dan 'kelas' telah ditambah ke dalam jadual 'karangan'!")
except sqlite3.OperationalError:
    print("⚠️ Lajur mungkin sudah wujud atau terdapat ralat lain.")

conn.close()
