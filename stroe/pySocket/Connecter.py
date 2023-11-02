
import socket
from  ConnectFrame import ConnectionFrame
from threading import Lock,Thread

class Connecter():
    def __init__(self,root) -> None:
        self.socket=socket.socket()
        self.ip=socket.get(socket.gethostname())
        self.port='15480'
        self.password=''
        self.ui=ConnectionFrame(root,[self.ip,self.port,self.password])
        self.state=0
        self.count=0
        self.clients = []  # 客户端列表
        self.number=0    #客户端数量
        self.lock=Lock()
        # self.ui.bind(self.buildRoom,self.connect)
    
    def setState(self, s):
        self.state = s

    def add(self):
        '''线程锁修改值'''
        self.lock.acquire()
        self.count+=1
        self.lock.release()
    
    def serverForClient(self, soc, adr):
        pass
        
    def client(self, soc, adr):
        """ 接收信息，重现操作 """
        while True:
            try:
                size = soc.recv(2)
                if size == b'':
                    break
                size = int(size)
                print('Will recvive', size, flush=True)
                mes = soc.recv(size)
                print(mes.decode(), flush=True)
            except Exception as e:
                print('Error when recving', e)
    
    def listen(self):
        """ 监听 """
        while True:
            try:
                dataSocket, adr = self.socket.accept()
                # self.number+=1
                th = Thread(target=self.serverForClient, args=(dataSocket,adr))
                th.start()
            except Exception as e:
                print('Exception when listen.', e)
                break
            
    def buildRoom(self):
        '''用本地socket作为服务器，建立房间'''
        if self.state == 1:
            return self.destoryRoom()
        elif self.state == 2:
            print('请先断开与其他主机的连接！')
            return
        # info = self.getIPAndPort()
        self.ui.buildRoom()
        self.socket.listen(10)
        th = Thread(target=self.listen, args=())
        th.start()

    def destoryRoom(self):
        '''终止socket作为服务器运行的行为'''
        self.setState(0)
        self.ui.destoryRoom()

    def connect(self):
        '''socket连接远程服务器'''
        if self.state == 2:
            return self.disconnect()
        elif self.state == 1:
            print('请先关闭本地服务！')
            return
        self.setState(2)
        self.ui.connect()

    def disconnect(self):
        '''socket断开与主机的连接'''
        self.setState(0)
        self.ui.disconnect()

    def send(self,mes):
        '''Call to send message.在前边的两字节标明长度'''
        size=len(mes)
        if size <10:
            size='0'+str(size)
        else:
            size=str(size)
        self.socket.sendall(size+mes)

    def handle(self,mes):
        # 处理接受的信息
        s=mes.split('_')
        s=[int(i) for i in s]
        if s[0]==0:
            pass
        
    # def isten
    
# if __name__=='__main__':
#     root
#     cnt=Connecter()