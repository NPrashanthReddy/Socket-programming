
import socket 
import threading
import os
import tqdm

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

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
			message = client.recv(BUFFER_SIZE).decode('utf-8')
			temp=message
			if temp[:2]=='>>':
				filename, filesize = temp.split(SEPARATOR)
				print(filename,filesize)
				filename_new="2"+filename[3:]
				filename_new = os.path.basename(filename_new)
				filesize=int(filesize)
				res=""
				
				while True:
					# read 1024 bytes from the socket (receive)
					print('lol')
					bytes_read = client.recv(BUFFER_SIZE)
					# if not bytes_read:    
					# 	# nothing is received
					# 	# file transmitting is done
					# 	break
					
					# write to the file the bytes we just received
					#f.write(bytes_read)
					#f.write(b'12345')						
					# res=res+bytes_read.decode("utf-8")
					# print(res,bytes_read,'lll')
					f=open(filename_new, "wb")
					f.write(bytes_read)
					f.close()
					break
					# update the progress bar
				# with open(filename_new,'w') as f:
				
			else:
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