
import socket 
import threading
import os
import tqdm

BUFFER_SIZE = 1024*512 #1/2MB
SEPARATOR = "<SEPARATOR>"

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("", PORT))

server.listen()
print('The server is up and running: listening too...')
clients = []
usernames = []


def broadcast(message):
	for client in clients:
		client.send(message)

def broadcast_file(send_client,filename,s_file):
	for client in clients:
		if client != send_client:
			file_send(client,filename,s_file)
	
def sendall(client,data,flag=0):
	sent=client.send(data,flag)
	if sent>0:
		return sendall(client,data[sent:],flag)
	else:
		return None


def file_send(client, filename,s_file):
	filesize = os.path.getsize(filename)
	client.send(f">> {s_file}{SEPARATOR}{filesize}".encode("utf-8")) #
	with open(filename,"rb") as f:
		while True:
			# read the bytes from the file
			bytes_read = f.read(BUFFER_SIZE)
			if not bytes_read:
				# file transmitting is done
				break
			# we use sendall to assure transimission in 
			# busy networks
			sendall(client,bytes_read)
			

def handle(client):
	while True:
		try: 
			message = client.recv(BUFFER_SIZE).decode('utf-8')
			temp=message
			if temp[:2]=='>>':
				filename, filesize = temp.split(SEPARATOR)
				print(filename,filesize)

				if not os.path.isdir('server'): os.makedirs('server') 
				filename_new=filename[3:]
				send_file=filename_new
				filename_new = os.path.join("server",filename_new)
				filesize=int(filesize)
				
				bytes_read = client.recv(BUFFER_SIZE)
				with open(filename_new, "wb") as f:
					f.write(bytes_read)
				

				broadcast_file(client,filename_new,send_file)
				
				
			else:
				# General text message
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
		username = client.recv(BUFFER_SIZE).decode('utf-8') #1024 bytes
		

		usernames.append(username)
		clients.append(client)

		print(f"User took a name of {username}")
		client.send(f"You've justed joined the chat\n Welcome to babel {username}\n".encode("utf-8"))
		broadcast(f"{username} joined the chat!\n".encode('utf-8'))

		thread = threading.Thread(target=handle, args=(client,))
		thread.start()

receive()