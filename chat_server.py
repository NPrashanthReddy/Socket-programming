
import socket 
import threading


HOST = socket.gethostbyname(socket.gethostname())
PORT = 9091
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(HOST)
server.bind(("", PORT))

server.listen()
print('The server is up and running: listening too...')
clients = []
usernames = []

# def send_file(client, filename):
# 	f"{username}/{filename}"
def broadcast(message):
	for client in clients:
		client.send(message)

def handle(client):
	while True:
		try: 
			message = client.recv(1024).decode('utf-8')
			if len(message) < 1:
				break
			print(f"{message}") #logging the information
			
			broadcast(message.encode('utf-8'))

		except: #if the client is crashed
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
		client.send(f"You've justed joined the chat\n Welcome to babel {username}\n".encode("utf-8"))
		broadcast(f"{username} joined the chat!\n".encode('utf-8'))

		thread = threading.Thread(target=handle, args=(client,))
		thread.start()

receive()