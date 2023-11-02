
from ConnectFrame import ConnectionFrame
from ui import ConnectUI
# from chatBox import ChatBox
# from function import changeImageWithName
from tkinter import  * # Tk,Frame
from time import time
from Connecter import Connecter

begin=time()

def testAll():

    root = Tk()
    #w = r.winfo_screenwidth()
    #h = r.winfo_screenheight()-100
    w, h = 1280, 800
    root.geometry("%dx%d+0+0" % (w, h))
    r = root
    root = Label(root, bg='burlywood')
    root.place(relwidth=1, relheight=1)
    cu = ConnectUI(root)
    # changeImageWithName(root,'bg')
    # r.bind('<space>',)
    r.mainloop()
    
def testIPInfo():
    root=Tk()
    #w = r.winfo_screenwidth()
    #h = r.winfo_screenheight()-100
    w, h = 300, 200
    root.geometry("%dx%d+0+0" % (w, h))
    r=root
    root = Label(root, bg='#DBCCB1')
    root.place(relwidth=1,relheight=1)
    cu = ConnectionFrame(root)
    # changeImageWithName(root,'bg')
    def getIP(*event):
        print(cu.getIPAndPort())
    r.bind('<Control-e>', getIP)
    print(time()-begin)
    r.mainloop()

def testConnecter():
    root = Tk()
    #w = r.winfo_screenwidth()
    #h = r.winfo_screenheight()-100
    w, h = 300, 200
    root.geometry("%dx%d+0+0" % (w, h))
    r = root
    root = Label(root, bg='#DBCCB1')
    root.place(relwidth=1, relheight=1)
    cu = Connecter(root)
    # changeImageWithName(root,'bg')

    def getIP(*event):
            print(cu.getIPAndPort())
    r.bind('<Control-e>', getIP)
    print(time()-begin)
    r.mainloop()

# testIPInfo()
# testConnecter()
testAll()

# if False:
#     pass
#输入ip与Port的文本框，以及对应密码，相应的连接相关按钮
# ip_port=Frame(root,relief='sunken')
# ip_port.place(relx=0,rely=0,relheight=0.2,relwidth=0.35)

# 显示连接与房间信息的消息框,以及聊天功能？

#显示房间人员信息的玩家框，以及相应的变更自身信息的操作

#开始游戏按钮（房主），返回主界面按钮
