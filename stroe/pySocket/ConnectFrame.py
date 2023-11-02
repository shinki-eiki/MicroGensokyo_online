
from tkinter import Radiobutton, Entry, Label, Button, StringVar
# from tkinter import ttk


class ConnectionFrame():
    '''记录IP与端口信息，用于网络连接'''
    # Title=['未连接','已建立服务','已连接主机','',]
    # Text = ['建立主机', '终止服务', '连接主机', '断开连接']

    def __init__(self, root,di) -> None:
        self.buildFrame(root,di)

    def buildFrame(self, root,defaultInfo=['114.5.1.4','15480','']) -> None:
        '''create all the button.'''
        bw = '2px'
        st = {'bg': "#94AA67", 'borderwidth': bw,  # 'foreground': "black",
              'font': '黑体 18'}
        text = ['IP', '端口', '密码']

        # 标题部分
        self.title = StringVar(value='未连接')
        t=Label(root,textvariable=self.title,**st)
        t.place(relx=0.1,rely=0,relwidth=0.8,relheight=0.18)
        
        #输入部分
        self.textLabels = [Label(root, text=text[i], **st) for i in range(3)]
        self.entry = [Entry(root, textvariable=StringVar(root,
            defaultInfo[i]),**st) for i in range(3)]
        self.entry[2]['show']='*'
        
        dx, dy, delta = 0.25, 0.2, 0.02
        for i in range(3):
            self.textLabels[i].place(relx=0,  rely=0.2+dy*i, relwidth=dx-delta, relheight=dy-delta)
            self.entry[i].place(relx=dx, rely=0.2+dy * i,relwidth=1-dx-delta*2, relheight=dy-delta)

        # 按钮部分
        # self.state = 0
        # 状态码：0 未确定 1作为主机 2 作为客户
        self.stateCode = ['未连接', '服务启动中', '已连接服务器']
        self.buttonText = [StringVar(value='建立主机'), StringVar(value='连接主机')]
        self.serverButton = Button(root, textvariable=self.buttonText[0], command=self.buildRoom)
        self.cilentButton = Button(root, textvariable=self.buttonText[1], command=self.connect)
        self.serverButton.place(
            relx=0.2, rely=0.8, relheight=0.2-delta, relwidth=0.3-delta)
        self.cilentButton.place(
            relx=0.5, rely=0.8, relheight=0.2-delta, relwidth=0.3-delta)

    def bind(self,sb,cb):
        self.serverButton.bind(sb)
        self.cilentButton.bind(cb)

    def setState(self,s):
        self.title.set(self.stateCode[s])
        
    def buildRoom(self):
        '''用本地作为服务器，建立房间'''
        self.setState(1)
        self.buttonText[0].set(value='终止服务')

    def destoryRoom(self):
        '''终止本地作为服务器运行的行为'''
        self.setState(0)
        self.buttonText[0].set(value='建立主机')

    def connect(self):
        '''连接远程服务器'''
        self.setState(2)
        self.buttonText[1].set(value='断开连接')

    def disconnect(self):
        '''断开与主机的连接'''
        self.setState(0)
        self.buttonText[1].set(value='连接主机')

    def setTexture(self):
        # set the color and theme as you like
        return

    def getIPAndPort(self):
        # return ip and port to connect.
        return [i.get() for i in self.entry]

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
