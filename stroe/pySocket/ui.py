
from tkinter import Radiobutton, Entry, Label, Frame
from ConnectFrame import ConnectionFrame


class ConnectUI():
    def __init__(self, root) -> None:
        '''左上角网络连接的数据，右下角是消息以及系统信息框，中间是房间信息框，右上角是头像框？
        右下角是准备和开始游戏、返回主界面按钮.大致分三个纵列'''
        base=0.25
        x = [0, 0, base, 0.8, 0.8]
        y = [0, 0.4, 0, 0, 0.8]
        spanWidth = [base, base, 0.8-base, 0.2, 0.2]
        spanHeight = [0.4, 0.6, 1, 0.8, 0.2]
        backColor = ['#E9CAA6', 'lightgray']
        frame = [Frame(root, bg=backColor[i & 1], borderwidth='2px')
                 for i in range(5)]
        delta = 0.01
        for i in range(5):
            frame[i].place(
                relx=x[i], rely=y[i], relheight=spanHeight[i]-delta, relwidth=spanWidth[i]-delta)

        self.socker = (frame[0])
        # self.message = (frame[1])
        # self.roomInfo = (frame[2])
        # self.other = (frame[3])
        # self.button = (frame[4])
        # self.ip_port = ConnectionInfo(root)

    def getIPAndPort(self, *event):
        return self.ip_port.getIPAndPort()
