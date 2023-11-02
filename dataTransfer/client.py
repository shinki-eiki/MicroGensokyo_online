

import socket

s=socket.socket(
    socket.AF_INET,socket.SOCK_STREAM
)

host=socket.gethostname()
port=15480

s.connect((host,port))

mess=s.recv(1024)

s.close()

print(mess.decode('utf-8'))