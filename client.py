import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 1234))

message = client.recv(1024).decode()
action = input(message)
client.send(action.encode())

message = client.recv(1024).decode()
client.send(input(message).encode())
message = client.recv(1024).decode()
client.send(input(message).encode())

print(client.recv(1024).decode())
