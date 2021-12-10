import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("3.110.132.40",8090))
s.send("Hello from hyd".encode())
print(s.recv(1024).decode())