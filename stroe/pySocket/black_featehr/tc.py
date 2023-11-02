
#客户端，循环发送

from socket import *
from time import sleep

IP='127.0.0.1'
SERVER_PORT=15480
BUFLEN=1024

dataSocket=socket(AF_INET,SOCK_STREAM)
# dataSocket.settimeout(0)
# dataSocket.setblocking(0)
print('Ready.')
try:
    dataSocket.connect((IP, SERVER_PORT))
except Exception as e:
    print('Exception when connecting!',e)
print('Connect!')

try:
    while True:
        size = dataSocket.recv(2)
        if size==b'':
            break
        size = int(size)
        print('Will recvive', size,flush=True)
        mes = dataSocket.recv(size)
        print(mes.decode(),flush=True)
except Exception as e:
    print('Error when recving',e)
finally:
    dataSocket.close()

dataSocket.close()



# toSend = input('>>>')
# if toSend == '':
#     break
# dataSocket.send(toSend.encode())

# recv = ''
# print('Recving...')
# try:
#     recv = dataSocket.recv(BUFLEN)
# except Exception as e:  # BlockingIOError:
#     print('Exception:', e)
#     print(recv.encode())
#     # 如果接受为空，代表对方关闭了连接
# # print('Recycle...')
# print('Handling...')
# # if not recv:
# #     if input('Exit?:')=='y':
# #         break
# # elif recv[-1]=='':
# # else:
# print(recv.decode())
