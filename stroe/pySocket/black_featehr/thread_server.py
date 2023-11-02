#  === TCP 服务端程序 server.py ， 支持多客户端 ===
# 含GUI的多客户服务器

# 导入socket 库
from socket import *
from threading import Thread
from tkinter import *
from time import sleep

root=Tk()
listenSocket = socket(AF_INET, SOCK_STREAM)
clients: list[socket] = []

def connectFun():

    # IP = ''  #外网可见
    IP='127.0.0.1' #本机可见
    PORT = 15480
    BUFLEN = 512
    count=0

    # 这是新线程执行的函数，每个线程负责和一个客户端进行通信
    def clientHandler(dataSocket:socket, addr,index):
        clients.append(dataSocket)
        def justSend():
            s = input(str(index)+'-message:')
            if s=='':return True
            size=len(s)
            if size<10:
                size='0'+str(size)
            else:
                size=str(size)
            s=size+s
            # dataSocket.send(size.encode())
            dataSocket.send(s.encode())
            return False
            
        def justAccept():
            recved = dataSocket.recv(BUFLEN)
            # 当对方关闭连接的时候，会返回空字符串
            if not recved:
                print(f'客户端{addr} 关闭了连接')
                return True
            info = recved.decode()
            print(f'收到{addr}信息： {info}')
            dataSocket.send(f'服务端接收到了信息 {info}'.encode())
            msgText.set(info)
            rb.place(x=0, y=0)
            return False
        
        while True:
            try:
                if justSend():
                    break
            except Exception as e:
                print('Exception when handle!', e)
                break
        print('Normally close socket',index)
        dataSocket.close()
        print(clients)
        
    listenSocket.bind((IP, PORT))
    listenSocket.listen(1)
    print(f'服务端启动成功，IP为{listenSocket.getsockname()},在{PORT}端口等待客户端连接...')

    while True:
        # 在循环中，一直接受新的连接请求
        # Establish connection with client.
        try:
            dataSocket, addr = listenSocket.accept()
            addr = str(addr)
            print(f'一个客户端 {addr} 连接成功')
            sleep(1)

            # 创建新线程处理和这个客户端的消息收发
            th = Thread(target=clientHandler, args=(dataSocket, addr,count))
            th.start()
            count += 1
        except Exception as e:
            # print(e)
            print('Exception when listen!',e)
            break

    # listenSocket.close()
    # if listenSocket
    # root.quit()
    # root.destroy()

th = Thread(target=connectFun, args=())
th.start()

def closeServer(*e):
    print(clients)
    for i in clients:
        # i.
        i.close()
    listenSocket.close()

msgText=StringVar(value='Hello.')
rb=Button(root,textvariable=msgText,command=closeServer)
rb.place(x=0,y=0)

root.mainloop()
