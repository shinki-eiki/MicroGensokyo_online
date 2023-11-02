
import socket

serverScoket=socket.socket(
    socket.AF_INET,socket.SOCK_STREAM
)

host=socket.gethostname()
port=15480

serverScoket.bind((host,port))

serverScoket.listen(3)

while 1:
    client,addr=serverScoket.accept()

    print(f'连接地址：{addr}')

    mess='Hello World!'
    # mess='Hello World!'+"\r\n"
    client.send(mess.encode('utf-8'))
    client.close()