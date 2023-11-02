
import socket
import _thread
import threading

class NetWindow:
    def __init__ (self,root) -> None:
        # self
        pass

        
class Server:

    def __init__(self,port=15480,passport=114514) -> None:
        host=socket.gethostbyname()
        self.server = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        while 1:
            finish=True
            try:
                self.server.bind((host,port))
            except :
                finish=False
                port+=1
            if finish:break
        self.passport=passport
        self.canConnect=True
        self.clients=[]
        print('绑定完成，地址-端口-密码\n{host} {port} {passport}')
        _thread.start_new_thread(self.wait)

    def wait(self):
        while 1:
            client,addr=self.server.accept()
            print(f'{addr}连接中')
            # ask='请输入密码：'+'\r\n'
            # client.send(ask.encode('utf8'))
            # try:
            #     pp = client.recv(1024)
            #     if pp == self.passport:

            self.clients.append(client)
    
    def handler(self,client):
        pass

    # def handleMessage():
    #     pass

if __name__ =='__main__':
    print('Hello')