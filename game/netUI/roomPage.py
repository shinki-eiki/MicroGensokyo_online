
from tkinter import Radiobutton, Entry, Label, Frame,Button, END
from tkinter.scrolledtext import ScrolledText

from .ConnectFrame import ConnectionFrame
from .room import Room
# import information
from ..information import Info

class RoomPage():
    """ 用于主机之间相互连接的总页面 """
    
    def __init__(self, root,sup=None,gameUI=None) -> None:
        '''左上角网络连接的数据，右下角是消息以及系统信息框，中间是房间信息框，右上角是头像框？
        右下角是准备和开始游戏、返回主界面按钮.大致分三个纵列'''

        self.root:Frame=root
        """ 由父类创建并分配的一个总框体 """
        self.father=sup
        self.exFunction = gameUI
        # 放置大的Frame
        base=0.25
        x =          [0, 0, base, 0.8, 0.8]
        y =          [0, 0.3, 0, 0, 0.8]
        spanWidth =  [base, base, 0.8-base, 0.2, 0.2]
        spanHeight = [0.3, 0.7, 1, 0.8, 0.2]
        backColor = ['lightgray', 
                     'lightgray',
                     '#E9CAA6',
                    ]
        frame = [Frame(root, bg=backColor[i & 1], borderwidth='2px') for i in range(5)]
        delta = 0.01
        for i in range(5):
            frame[i].place(
                relx=x[i], rely=y[i], relheight=spanHeight[i]-delta, relwidth=spanWidth[i]-delta)

        # 初始化类成员
        self.InfoFrame = ConnectionFrame(frame[0],self)
        # self.message = (frame[1])
        self.roomInfo = Room(frame[2],self)
        # self.other = (frame[3])
        # self.button = (frame[4])

        #按钮部分
        self.beginButton = Button(
            frame[4], text='开始游戏', state='disable', command=self.beginGame)
        self.changeButton = Button(
            frame[4], text='游戏界面', command=self.toGameUI)
        self.quitButton = Button(
            frame[4], text='返回', command=self.quit)

        bh = 0.338
        self.buttons = [self.beginButton, self.changeButton, self.quitButton]
        for i,v in enumerate(self.buttons):
            v.place(relx=0.2, rely=i*bh,   relwidth=0.6, relheight=bh-0.02)

        #消息显示框
        self.message = ScrolledText(frame[1], undo=True, fg='lightgreen', cursor='pencil',
            font='黑体 13', bg='grey')
        self.message.place(relwidth=1, relheight=1)
        Info.roomPage=self

    def place(self):
        self.root.place(relx=0.1,rely=0.05,relheight=0.9,relwidth=0.8)
    
    def place_forget(self):
        self.root.place_forget()

    def newMessage(self, *mes):
        """ 给信息加上当前事件再显示 """
        cur = Info.getTime()
        for text in mes:
            self.message.insert(END, '[%d]:%s\n' %
                (cur, text))  # cur+text+'\n',
            self.message.see(END)

    def getIPAndPort(self, *event):
        return self.InfoFrame.getIPAndPort()
    
    def buildRoom(self):
        self.InfoFrame.buildRoom()
        self.roomInfo.add()
        self.beServer()

    def destoryRoom(self):
        '''终止本地作为服务器运行的行为'''
        self.InfoFrame.destoryRoom()
        self.quitRoom()
        self.stopServer()

    def connect(self):
        '''连接远程服务器'''
        self.InfoFrame.connect()
        # Info.setThis()

    def disconnect(self):
        '''断开与主机的连接'''
        self.InfoFrame.disconnect()
        self.quitRoom()

    def quit(self):
        """ 退出roomPage页面，返回主界面 """
        # self.father.place_forget()
        self.root.place_forget()
        self.father.place()

    def stopServer(self):
        """ 当建立服务器时，使开始游戏按钮可用 """
        self.beginButton['state'] = 'disable'

    def beServer(self):
        """ 当终止服务器时，使开始游戏按钮不可用 """
        self.beginButton['state'] = 'normal'
    
    def quitRoom(self):
        """ 退出当前房间，清空信息 """
        self.newMessage('退出当前房间。\n-----------\n')
        self.roomInfo.clear()    
    
    def toGameUI(self):
        self.father.place_forget()
        self.exFunction()

    def beginGame(self,se=114514):
        self.newMessage(*Info.playerLabelList)

        #-----------
        cnt = Info.connecter
        if cnt.isServer():
            from random import randint
            se=randint(1,1<<28)
            cnt.send(f'1_{se}')
        # else:
        Info.setSeed(se)
        self.newMessage('游戏开始')
        self.father.startGame()
        # if self.beginGameFun!=None:
        #     self.beginGameFun()
    
    # def returnHome(self):
    #     # self.newMessage('是否返回首页？')
    #     self.root.place_forget()
