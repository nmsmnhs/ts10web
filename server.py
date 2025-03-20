import sqlite3
import hashlib
import threading
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 1234))

server.listen()

conn = sqlite3.connect("userdata.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS userdata (username TEXT UNIQUE, password TEXT)")
conn.commit()
conn.close()


def handle_connection(c):
    try:
        c.send("Type 'login' or 'register': ".encode())
        action = c.recv(1024).decode().strip().lower()

        c.send("Username: ".encode())
        username = c.recv(1024).decode().strip()

        c.send("Password: ".encode())
        password = c.recv(1024).decode().strip()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hash password

        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        if action == "register":
            try:
                cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, hashed_password))
                conn.commit()
                c.send("Registration successful.\n".encode())
            except sqlite3.IntegrityError:
                c.send("Error: Username already exists. Try again.\n".encode())

        elif action == "login":
            cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, hashed_password))
            if cur.fetchone():
                c.send("Login successful.\n".encode())
            else:
                c.send("Login failed: Incorrect username or password.\n".encode())


        conn.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        c.close()

while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client, )).start()