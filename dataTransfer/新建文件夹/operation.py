from .dataStorage import DataStorage as ds

def whenOperateion(fun):
    '''主要操作前后的处理'''
    # if True:#判断当前玩家
    #     return
    ds.setAdding()
    r=fun()
    if not r:return
    res=f'r_{ds.encore()}'
    return res

# ds.add(1)
# ds.show()
# 1获取卡牌
# 2使用卡牌
# 3发动设施
# 4捕获妖怪
# 5结束回合