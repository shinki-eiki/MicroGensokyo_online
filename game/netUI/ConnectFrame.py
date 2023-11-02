
from tkinter import Entry, Label, Button, StringVar,Frame,END
from tkinter.scrolledtext import ScrolledText
from ..information import Info
# import information

class ConnectionFrame():
    '''记录与修改IP与端口信息的窗体，用于网络连接'''
    # Title=['未连接','已建立服务','已连接主机','',]
    # Text = ['建立主机', '终止服务', '连接主机', '断开连接']

    def __init__(self, root, ui , di = ['127.0.0.1', '15480', '']) -> None:
        self.buildFrame(root,ui,di)

    def buildFrame(self, root,ui,defaultinfo) -> None:
        '''create all the button.包括输入框和信息框'''
        bw = '2px'
        st = {
            # 'bg': "",
            # 'bg': "#94AA67",
              'borderwidth': bw, 
              'font': '黑体 18',
              # 'foreground': "black",
            }
        text = ['IP', '端口', '密码']
        self.father=ui

        # 标题部分
        # root=Frame(root)
        # root.place(relwidth=1,relheight=0.3)
        self.title = StringVar(value='未连接')
        t = Label(root, textvariable=self.title, bg="#94AA67", **st)
        t.place(relx=0.1,rely=0,relwidth=0.8,relheight=0.18)
        
        # 输入部分
        self.textLabels = [Label(root, text=text[i], **st) for i in range(3)]
        self.entry = [Entry(root, textvariable=StringVar(root,
            defaultinfo[i]),**st) for i in range(3)]
        self.entry[2]['show']='*'
        
        dx, dy, delta = 0.25, 0.2, 0.02
        for i in range(3):
            self.textLabels[i].place(relx=0,  rely=0.2+dy*i, relwidth=dx-delta, relheight=dy-delta)
            self.entry[i].place(relx=dx, rely=0.2+dy * i,relwidth=1-dx-delta*2, relheight=dy-delta)

        # 按钮部分
        # self.state = 0
        # 状态码：0 未确定 1作为主机 2 作为客户
        self.stateCode = ['未连接', '服务已启动', '已连接服务器']
        self.buttonText = [StringVar(value='建立主机'), StringVar(value='连接主机')]
        # def fun1(*e):
        #     Info.connecter.buildRoom()

        # def fun2(*e):
        #     Info.connecter.connect()

        self.serverButton = Button(
            root, textvariable=self.buttonText[0], command=lambda: Info.connecter.buildRoom())
        self.cilentButton = Button(
            root, textvariable=self.buttonText[1], command=lambda: Info.connecter.connect())
        self.serverButton.place(
            relx=0.2, rely=0.8, relheight=0.2-delta, relwidth=0.3-delta)
        self.cilentButton.place(
            relx=0.5, rely=0.8, relheight=0.2-delta, relwidth=0.3-delta)

    def newMessage(self,*mes):
        self.father.newMessage(*mes)

    def setState(self,s):
        """ 因为逻辑不在这里处理，所以只是解决界面的变化 """
        self.title.set(self.stateCode[s])
        
    def buildRoom(self):
        '''用本地作为服务器，建立房间'''
        self.setState(1)
        self.buttonText[0].set('终止服务')
        info=self.getIPAndPort()
        self.newMessage(f'已建立房间，IP：{info[0]},端口为：{info[1]}\n')

    def destoryRoom(self):
        '''终止本地作为服务器运行的行为，理论上因为连接时已经给出信息了，所以断开时就不管了吧...'''
        self.setState(0)
        self.buttonText[0].set('建立主机')
        self.newMessage('终止服务。')

    def connect(self):
        '''连接远程服务器'''
        self.setState(2)
        self.buttonText[1].set('断开连接')
        info = self.getIPAndPort()
        self.newMessage(f'已进入房间，IP：{info[0]},端口为：{info[1]}\n')

    def disconnect(self):
        '''断开与主机的连接'''
        self.setState(0)
        self.buttonText[1].set('连接主机')
        self.newMessage('已断开连接。')

    def setTexture(self):
        """ set the color and theme as you like """
        return

    def bind(self, sb, cb):
        self.serverButton.bind(sb)
        self.cilentButton.bind(cb)

    def getIPAndPort(self):
        """ return ip and port to connect. """
        res=[i.get() for i in self.entry]
        res[1]=int(res[1])
        return res

# if __name__=='main':
#     root=Tk()

 # self.textLabels[i].place(
        #     relx=0,  rely=dy*i, relwidth=dx, relheight=dy)
        # self.entry[i].place(relx=dx, rely=dy * i,
        #                     relwidth=1-dx, relheight=dy)
        
# t = ['建立主机', '停止服务', '连接主机','断开连接'  ]
        # self.button=[
        #     Button(root, text=t[0],command=self.buildRoom),
        #     Button(root, text=t[1],command=self.destoryRoom,state='disabled'),
        #     Button(root, text=t[2],command=self.connect),
        #     Button(root, text=t[3],command=self.connect,state='disabled'), ]
