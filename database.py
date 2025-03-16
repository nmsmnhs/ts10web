import sqlite3
import hashlib

conn = sqlite3.connect("userdata.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
    id INTEGRE PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")


user1, pass1 = "mikeoxlongjkdfj", hashlib.sha256("mikeoxshort".encode()).hexdigest()
user2, pass2 = "mikeoxgigantic", hashlib.sha256("mycateatspebbles".encode()).hexdigest()
cur.execute("INSERT INTO  userdata (username, password) VALUES (?, ?)", (user1, pass1))
cur.execute("INSERT INTO  userdata (username, password) VALUES (?, ?)", (user2, pass2))


cur.execute("DELETE FROM userdata")

conn.commit()
conn.close()

# this is just me messing with sql stuff, dont mind it, idk if deleting it does anything yet so im keeping it here for now ig
