
from game.netUI.ConnectFrame import ConnectionFrame
from game.netUI.Connecter import Connecter
from game.netUI.roomPage import RoomPage
from game.information import Info
# from game.netUI.roomPage import RoomPage

from tkinter.simpledialog import askinteger
from tkinter import Label,Tk  # Tk,Frame
from time import time
from random import randint

# from chatBox import ChatBox
# from function import changeImageWithName

begin = time()
cnt = 0

def testAll():
    root = Tk()
    w, h = 1080, 600
    root.geometry("%dx%d+0+0" % (w, h))

    baseRoot = root
    root = Label(root, bg='lightslategray')
    root.place(relwidth=1, relheight=1)
    # changeImageWithName(root,'bg')

    name = ['reimu', 'marisa', 'alice','youmu', 'sakuya', 'sanae', 'aya']
    rp = RoomPage(root,baseRoot)
    r = rp.roomInfo

    def add(*e):
        global cnt
        # rp.roomInfo.add(name[cnt % 6]+str(randint(1,114514)), cnt%12, cnt % 3)
        rp.roomInfo.add()
        cnt += 1

    def remove(*e):
        print('Call remove.')
        t = askinteger(title='Which one?', prompt='The index:')
        if t != None:
            r.remove(t)

    def change(*e):
        i = askinteger('', 'Who?')
        t = askinteger(title='Which property?', prompt='The code:')
        if t != None:
            r.change(i, t)

    def collect(*e):
        print(*Info.getPlayerInfo())

    baseRoot.bind('<Control-a>', add)
    baseRoot.bind('<Control-r>', remove)
    baseRoot.bind('<Control-c>', change)
    baseRoot.bind('<Control-g>', collect)
    baseRoot.bind('<Control-e>', rp.quitRoom)
    Info.connecter=Connecter()
    baseRoot.mainloop()

def testIPInfo():
    root = Tk()
    w, h = 300, 600
    root.geometry("%dx%d+0+0" % (w, h))
    r = root
    root = Label(root, bg='#DBCCB1')
    root.place(relwidth=1, relheight=1)
    cu = ConnectionFrame(root)
    # changeImageWithName(root,'bg')

    def getIP(*event):
        print(cu.getIPAndPort())

    def dest(*e):
        cu.destoryRoom()

    def dis(*e):
        cu.disconnect()

    r.bind('<Control-e>', getIP)
    r.bind('<Control-d>', dest)
    r.bind('<Control-c>', dis)
    print(time()-begin)
    r.mainloop()

def testConnecter():
    root = Tk()
    w, h = 300, 200
    root.geometry("%dx%d+0+0" % (w, h))
    r = root
    root = Label(root, bg='#DBCCB1')
    root.place(relwidth=1, relheight=1)
    cu = ConnectionFrame(root)
    # cu = Connecter(root)
    # changeImageWithName(root,'bg')

    def getIP(*event):
        print(cu.getIPAndPort())

    r.bind('<Control-e>', getIP)
    print(time()-begin)
    r.mainloop()


def testConnecter2():
    cnt=Connecter()
    print(cnt.preprocessing('0_0_1'))

# testIPInfo()
# testConnecter()

testAll()
# testConnecter2()
# test

# if False:
#     pass
# 输入ip与Port的文本框，以及对应密码，相应的连接相关按钮
# ip_port=Frame(root,relief='sunken')
# ip_port.place(relx=0,rely=0,relheight=0.2,relwidth=0.35)

# 显示连接与房间信息的消息框,以及聊天功能？

# 显示房间人员信息的玩家框，以及相应的变更自身信息的操作

# 开始游戏按钮（房主），返回主界面按钮
