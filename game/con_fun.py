

from dataTransfer.dataStorage import DataStorage as ds
from .information import Info
from .netMessage import NetMessage
# from time import sleep

def afterOperation(mes:str):
    """ 本地操作之后，将组织好的完整消息内容发送，通知其他玩家 """
    # import netUI.Connecter
    if len(mes)==0:
        return
    print('Sending operation',mes,flush=True)
    c = Info.connecter
    c.send( mes )

def whenOperateion(fun):
    '''主要操作前后的处理，操作前后的ds都是normal状态
    利用ds是否可以取值区分是在操作还是重现,
    只需要函数执行操作并返回操作码即可，操作记录由ds获取'''
    
    def inner(*args,**kw):
        # 如果能够取值，代表正在重复，直接本地运行一遍，不传递操作,recur走这一步
        if ds.canGet():
            # print('Repeat operation.',flush=1)
            fun(*args, **kw)
            ds.setNormal()
            return
        
        # 本地玩家主动点击走这一步，开启记录模式
        ds.setAdding()
        ni = NetMessage.instance
        ni.setHead('2_')
        # print('Operation.',flush=1)
        r = fun(*args, **kw)
        if r==False: #操作无效
            ds.clear()
            # ds.setNormal()
            ni.clear()
        else:
            afterOperation( ni.getMessage())
        ds.setNormal()
    return inner

def whenAsk(fun):
    '''在等待玩家操作前，确认是否已有值待取'''
    # return fun
    def inner(*arg, **kw):
        '''return fun(*arg) if Gui.ds.isEmpty() else Gui.ds.get()'''
        if ds.hasVal(): #能取值，就直接获取
            # sleep(0)
            return ds.get()
        else:  # 不能取值，就走流程询问，并存储
            # ds.setAdding()
            res = fun(*arg, **kw)
            ds.add(res)
            # ds.setNormal()
            return res
    return inner

def testPrint(*s):
    for i in s:
        print(i)