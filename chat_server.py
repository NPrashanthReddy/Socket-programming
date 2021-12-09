from ctypes import addressof
import socket 
import threading
from tkinter import Message

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(HOST)
server.bind((HOST, PORT))

server.listen()
print('The server is up and running: listening too...')
clients = []
usernames = []

def broadcast(message):
	for client in clients:
		client.send(message)

def handle(client):
	while True:
		try: 
			message = client.recv(1024).decode('utf-8')
			print(f"{usernames[clients.index(client)]}: {message}")
			broadcast(message.encode('utf-8'))

		except:
			index = clients.index(client)
			clients.remove(client)
			client.close()

			usernames.pop(index)
			break

def receive():
	while True:
		client, address = server.accept()
		print(f"Connected with {str(address)}")

		client.send("USERNAME".encode("utf-8"))
		username = client.recv(1024).decode('utf-8') #1024 bytes

		usernames.append(username)
		clients.append(client)

		print(f"User took a name of {username}")
		broadcast(f"{username} joined the chat!\n".encode('utf-8'))
		client.send(f"You've justed joined the chat\n Welcome to babel {username}".encode("utf-8"))

		thread = threading.Thread(target=handle, args=(client,))
		thread.start()

receive()