
from dataTransfer.dataStorage import DataStorage as ds

class NetMessage():
    """ 用于组织在网络中传递的字节信息 
    包括 头部-操作细节-操作数据 三部分"""

    instance: "NetMessage" = None
    opMap={
        'gain': 1,
        'use': 2,
        'launch': 3,
        'catch': 4,
        'end': 5,
        'next': 6,
        'spell': 7,
        'miracle': 8,
    }

    def __init__(self) -> None:
        self.head=''
        self.operation=''

    def add(self,op): 
        """ 给head加上字符 """
        self.head+=str(op)

    def setHead(self,op):
        """ 给head重新赋值 """
        self.head=str(op)

    def getMessage(self):
        res = f'{self.head}{ds.encode()}'
        self.clear()
        return res
    
    def clear(self):
        """ 清空 """
        self.head=''

NetMessage.instance=NetMessage()