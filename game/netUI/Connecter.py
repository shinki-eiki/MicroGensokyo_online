
import socket
from threading import Lock, Thread
from random import randint
from time import sleep
from tkinter.messagebox import askyesno

# from .ConnectFrame import ConnectionFrame
# import information
from ..information import Info
from dataTransfer.dataStorage import DataStorage as ds


class Connecter():
    """ IP和端口等后端信息,以及通信socket """
    headLength = 4

    def __init__(self,*e) -> None:
        self.socket = None  # socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = '127.0.0.1'
        self.port = '15480'
        self.password = ''
        # self.ip=socket.gethostbyname(socket.gethostname())

        self.ui = Info.roomPage

        self.state = 0
        """ 当前状态,0为未确定,1为作为服务器,2为作为客户端 """
        self.count = 0
        """ 服务器用变量,用于在收各个客户端玩家的选择操作时计数 """
        self.clients: list[socket.socket] = []
        """  客户端列表 """
        self.number = 0
        """  服务器用变量,代表连接的客户端数量（包括 """
        self.lock = Lock()
        self.data=[0]*20
        # self.ui.bind(self.buildRoom,self.connect)
        # Info.roomPage.newMessage('本地IP及端口',self.ip,self.port)
        # Info.connecter=self

    def newSocket(self):
        # if self.socket == None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.settimeout(600)
        # ip,port,_=self.ui.getIPAndPort()
        # self.socket.bind((ip,port))

    def clear(self):
        """ 不论C和S,只要离开房间就调用的清理函数 """
        self.setState(0)
        self.count = self.number = 0

        for i in self.clients:
            try:
                # i.shutdown(socket.SHUT_RDWR)
                i.close()
            except OSError:
                print('Error when shutdown and close.',self.clients)
        self.clients.clear()

        if self.socket != None:
            try:
                # self.socket.settimeout(0)
                # self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
            except OSError:
                print('Error when shutdown and close.', self.clients)
        self.socket = None

    def setState(self, s):
        self.state = s

    def isUnsure(self): return self.state == 0
    def isServer(self): return self.state == 1
    def isClient(self): return self.state == 2

    def add(self):
        '''线程锁修改值'''
        self.lock.acquire()
        self.count += 1
        self.lock.release()

    def deleteClient(self,soc):
        """ 从客户端列表和房间中移除某一玩家 """
        for i, v in enumerate(self.clients):
            if v == soc:
                self.clients.pop(i)
                self.number-=1
                mes = self.preprocessing(f'0_1_{i+1}')
                self.sendToCilents(soc, mes)
                Info.roomPage.roomInfo.remove(
                    i+1)  # 由于自身是不存在客户端列表中,所以+1
                break

    def buildRoom(self):
        '''用本地socket作为服务器,建立房间'''
        # 前置条件判断
        if self.state == 1:
            """ 如果已建立房间,则终止该房间 """
            return self.destoryRoom()
        elif self.state == 2:
            print('请先断开与其他主机的连接！')
            return

        # 绑定与开启监听
        ip, port, _ = self.ui.getIPAndPort()
        self.newSocket()
        self.socket.bind((ip, port))
        self.socket.listen(10)
        th = Thread(target=self.listen, args=())
        th.start()

        # 后处理
        self.setState(1)
        self.ui.buildRoom()
        Info.setThis(0)

    def connect(self):
        '''通过socket,连接远程服务器'''
        # 前置条件判断
        if self.state == 2:
            return self.disconnect()
        elif self.state == 1:
            print('请先关闭本地服务！')
            return

        # 连接并设置本地在房间的编号
        self.newSocket()
        ip, port, _ = self.ui.getIPAndPort()
        self.socket.connect( (ip, port) )
        th = Thread(target=self.recvAsClient, args=())
        th.start()

        # 后处理
        self.setState(2)
        self.ui.connect()

    def preprocessing(self, mes :str) -> bytes:
        """ 预处理将要发送的信息:在头部的四字节标注长度,为了方便,传str会好点 """
        if isinstance(mes, bytes):
            mes = mes.decode()
        size = len(mes)
        s = str(size)
        mes = '0'*( self.headLength-len(s) )+s+mes
        return mes.encode()

    def sendToCilents(self, soc: socket.socket = None, mes: bytes = b''):
        """ 默认message经过预处理 """
        print('Send to Clients:',mes)
        if not self.isServer():
            return
        for _, v in enumerate(self.clients):
            if v != soc:
                v.sendall(mes)
            # else:
            #     print('Dont send to',v)

    def serverForClient(self, soc: socket.socket, adr):
        """ 服务器监听单个客户端的信息,该函数会并发执行多个以服务多个客户端 """
        print('Listen for',soc,'begin...')
        while True:
            try:
                # 先接受消息长度,判断是否为空
                size = soc.recv(self.headLength)
                if len(size) == 0:  # 被动断开
                    a = askyesno('断开连接？', f'与{soc}的连接已断开,是否重新连接？')
                    if a:
                        # self.connect()
                        continue
                    print('Disconnect:', soc, adr, flush=True)
                    self.deleteClient(soc)
                    break

                # 接受消息内容,并在本地处理
                size = int(size)
                # print('Will recvive', size, flush=True)
                mes = soc.recv(size)
                print(mes.decode(), flush=True)
                res = True # (mes[4]==b'3')
                # print('res',res)

                # 由于是服务器,所以需要分发到其他客户端,
                # 对于非当前玩家操作,需要全部接受之后再统一转发
                # 而其他操作基本是当前玩家发出,不需要确认谁的操作,原封不动转发即可
                if res :
                    self.sendToCilents( soc, self.preprocessing(mes) )
                self.handle(mes)
                # else:
                #     pass
            except Exception as e:
                self.ui.newMessage('Error when recving as server!', soc, e)
                print('Disconnect:', soc, adr, flush=True)
                self.deleteClient(soc)
                break

    def recvAsClient(self):
        """ 作为客户端接收服务器的信息,这时只有自己的一个socket需要接受,并且不考虑转发 """
        soc = self.socket
        while True:
            try:
                size = soc.recv(self.headLength)
                if len(size) == 0:  # 被动断开连接
                    a = askyesno('断开连接？', '与服务器的连接已断开,是否重新连接？')
                    if a:
                        self.setState(0)
                        self.connect()
                        continue
                    print('Disconnect:', soc, flush=True)
                    self.disconnect()
                    break

                # 客户端只需要处理信息,不考虑转发
                size = int(size)
                # print('Will recvive', size, flush=True)
                mes = soc.recv(size)
                print(mes.decode(), flush=True)
                self.handle(mes)
                
            except Exception as e:
                self.ui.newMessage('Error when recving as client!', e)
                self.disconnect()
                break
            # except TimeoutError

    def listen(self):
        """ 作为服务器监听连接并为客户端建立新socket """
        while True:
            try:
                # 存储socket,并且开启监听函数
                dataSocket, adr = self.socket.accept()
                th = Thread(target=self.serverForClient,
                            args=(dataSocket, adr))
                th.start()
                self.clients.append(dataSocket)

                # 建立连接后,本地添加玩家（使用默认配置）,然后发送房间信息
                Info.roomPage.roomInfo.add()
                for i, v in enumerate(Info.playerLabelList):
                    # 0_0_reimu_8_2
                    mes = self.preprocessing(f'0_0_{repr(v)}')
                    if i == len(Info.playerLabelList)-1:
                        self.sendToCilents(None,mes)
                    else:
                        dataSocket.sendall(mes)

                # 通信以指定其编号
                # print('New client:',dataSocket,flush=True)
                self.number += 1
                mes = f'0_3_{self.number}'
                dataSocket.send(self.preprocessing(mes))

                # 后处理
                # self.sendToCilents(self.preprocessing())
            except Exception as e:
                self.ui.newMessage('Exception when listenning.', e)
                break

    def send(self, mes: str ) -> str:
        '''发送信息,首先对其预处理:在前边的4字节标明长度,不足长度时补0
        作为服务器发送信息时,对所有客户端操作；

        作为客户端发送信息时,只通过自身的socket发送到服务器,再由服务器转发
        使用自带的socket,所以可以作为客服端发送信息
        由于此时发送消息时,双方是已知的,无需特别指定
        '''
        mes = self.preprocessing(mes)
        # print('State:',self.state)
        if self.isUnsure():
            return
        elif self.isServer():
            self.sendToCilents(None, mes)
        else:
            self.socket.sendall(mes)


    def handle(self, mes: bytes) -> bool:
        """ 处理接受的信息(默认用bytes传递),
        注意对于客户端和服务器,能接受到的信息不同 
        返回值决定服务器是否向其他客户转发"""
        if len(mes) == 0:
            return
        res = True
        s = mes.decode().split('_')
        op = int(s[0])
        if op == 0:  # 人员变动,包括增加,减少,以及信息修改
            # 0_0_0_0_0
            a = int(s[1])
            ri = Info.roomPage.roomInfo
            if a == 0:  # 增加
                # 0_0_reimu_8_2
                ri.add(s[2], int(s[3]), int(s[4]))
            elif a == 1:  # 移除
                # 0_1_1
                ri.remove(int(s[2]))
            elif a == 2:  # 修改属性
                # 0_2_1_1_name/res/image
                ri.setOneProperty(int(s[2]), int(s[3]), s[4])
            elif a == 3:  # 设置该玩家在房间的序号
                # sleep(1)
                Info.setThis(int(s[2]))

        elif op == 1:  # 开始游戏,传递一个随机数种子
            se = int(s[1])
            Info.roomPage.beginGame(se)

        elif op == 2:  # 操作重现,注意这只针对当前玩家

            from ..player import recur
            mes=mes.decode()
            # print('recur',mes)
            recur(mes[2:])

        elif op == 3:  # 奇迹时收集所有玩家操作信息,只有服务器会接受和处理
            self.setData( int(s[1]),int(s[2]) )
            res = False
            
            if self.count == self.number+1:
                # 当所有信息都收集时,向所有客户端发送列表
                sd=[ str(self.data[i]) for i in range(self.number+1) ]
                sd='_'.join(sd)
                print('Collect result:',sd,flush=1)
                self.sendToCilents( None ,self.preprocessing(f'4_{sd}') )

                for i in range(self.number+1):
                    ds.add(self.data[i])
                self.count = 0

        elif op == 4:  # 奇迹操作的集合传递,只有客户能接受
            print('All operations:', sd, flush=1)
            oldstate=ds.state
            ds.setAdding()
            for i in range(1,len(s)):
                ds.add(int(s[i]))
            ds.state=oldstate
            # ds.fillWithArray(self.data,0)
        else:
            print('Undefined!',mes)
        return res

    def destoryRoom(self):
        '''终止作为服务器运行的行为'''
        self.clear()
        self.ui.destoryRoom()

    def disconnect(self):
        '''socket断开与主机的连接'''
        self.clear()
        self.ui.disconnect()

    def setData(self,pi:int,v:int):
        """ 奇迹时设置数据 """
        if self.isUnsure():
            return
        elif self.isServer():
            self.add()
            self.data[pi] = v
        else:
            self.send(f'3_{pi}_{v}')

    # def 
    # def isten

if __name__=='__main__':
    cnt=Connecter()
    print( cnt.preprocessing('0_0_1') )
