
from time import time
from .function import findHeadImage

# from .netUI import playerLabel, roomPage, Connecter
# import netUI.playerLabel
# import netUI.roomPage
# import netUI.Connecter

class Info():
    """ 一些公用的信息 """

    defaultName = ['reimu', 'marisa', 'youmu', 'sakuya', 'sanae', 'aya']
    """ 默认玩家名字，循环轮调 """
    thisPlayer = 0
    """ 该玩家在房间的编号，对于服务器玩家默认为0，指定玩家使用这个编号 """
    currentPlayer = 0
    """ 当前回合玩家在房间的编号 """
    headImage = []
    """ 头像的集合 """
    beginTime = time()
    """ 初始化时的时间 """

    playerLabelList = []
    """ 房间玩家信息框列表  """
    roomPage= None
    """ RoomPage的指针 """
    connecter = None
    """ 网络连接类 """
    # resChar = ['★', '◎', '♨']

    # playerLabelList: list[netUI.playerLabel.PlayerLabel] = []
    # roomPage: roomPage.RoomPage = None
    # connecter: netUI.Connecter.Connecter = None
    # removeCount=0
    """ 房间中已退出的人数，目前废用 """

    @classmethod
    def setThis(cls, this=None):
        """ 设置本地玩家的标号 """
        if this==None:
            this=len(cls.playerLabelList)-1
        # 注意pl包含所有玩家，包括服务器
        cls.thisPlayer = this
        cls.playerLabelList[this].able()

    @classmethod
    def isCurrent(cls) -> bool:
        """ 该本地玩家是否当前玩家 """
        return cls.thisPlayer == cls.currentPlayer

    @classmethod
    def isThis(cls, p) -> bool:
        """ 某玩家是否本地玩家 """
        return cls.thisPlayer == p

    @classmethod
    def getTime(cls):
        '''返回程序已运行的时间'''
        return int(time()-cls.beginTime)

    @classmethod
    def getPlayerInfo(cls):
        """ 返回房间里的玩家信息，用于开始游戏 """
        return [(i.name, i.image, i.res) for i in cls.playerLabelList]

    @classmethod
    def getHeadImage(cls):
        """ 获取头像目录下的所有图片，保存到一起 """
        try:
            for i in range(10):
                cls.headImage.append(findHeadImage(i))
        except Exception:
            return

    @classmethod
    def setSeed(cls,s):
        """ 设定初始种子，所有玩家保持一致 """
        from random import seed
        seed(s)
        cls.roomPage.newMessage(f'Random seed ={s}')
        

# Info.getHeadImage()
