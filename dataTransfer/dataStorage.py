
from time import sleep

def testPrint(*s, **m):
    for i in s:
        print(i, **m)


class DataStorage:
    '''用一个大数组模拟的状态队列，该队列在连续操作中只能添加或者只能获取数据，'''

    @classmethod
    def init(cls) -> None:
        '''original length is 100. '''
        cls.data = [None]*100
        cls.cur = 0
        # 队列头部指针，这里指向的是当前头部元素（未取），队列为空时,指向0
        cls.ptr = 0  # 下一个插入的位置，即队列尾的下一个索引
        cls.state = 0
        # 队列是否正在添加，
        # 1代表只能添加，,2代表只能取值,初始时状态为0，不能取值也不能添加
        cls.waiting=False

    # -----------------下面五个函数只涉及状态码的改变，与队列的填充是否已满无关
    @classmethod
    def setNormal(cls):
        '''Set the state to be normal.We can not get or add. '''
        cls.state = 0

    @classmethod
    def setAdding(cls):
        '''Set the state to be add.We just can add value to it. '''
        cls.state = 1

    @classmethod
    def setGetting(cls):
        '''Set the state to be get.We just can get value from it. '''
        cls.state = 2

    @classmethod
    def canAdd(cls):
        return cls.state == 1

    @classmethod
    def canGet(cls):
        return cls.state == 2

    def setWaiting(cls,state=True):
        cls.waiting=state

    # --------------------------------------------------------------------

    @classmethod
    def hasVal(cls):
        '''队列能否取值,要求其状态可取值且队列不为空'''
        return cls.canGet()  # and (not cls.isEmpty())

    @classmethod
    def add(cls, val):
        '''向队列中添加一个值，'''
        if not cls.canAdd():
            return
        if cls.ptr >= len(cls.data):
            cls.data += [0]*10
        if isinstance(val, bool):
            cls.data[cls.ptr] = int(val)
        else:
            cls.data[cls.ptr] = val
        cls.ptr += 1

    @classmethod
    def waitForValue(cls) ->int:
        cnt = 0
        while cls.cur == cls.ptr:
            sleep(1)
            cnt += 1
            print('loop', cnt, flush=1)
            if cnt > 10:
                print('DS Overloop!', flush=1)
                return 0  # 出错时直接返回0
        return cls.get()
    
    @classmethod
    def get(cls):
        '''获取头部值'''
        # if not cls.hasVal():
        if not cls.canGet():
            testPrint('Can not get!')
            return -114
        
        if cls.waiting:
            return cls.waitForValue()
    
        res = cls.data[cls.cur]
        cls.cur += 1
        if cls.cur == cls.ptr:
            cls.clear()
        return res

    @classmethod
    def getAll(cls):
        '''获取所有值，然后清空'''
        res = cls.data[cls.cur:cls.ptr]
        cls.clear()
        return res

    @classmethod
    def isEmpty(cls):
        '''队列是否为空，目前只认为指针在前头时队列为空'''
        return cls.ptr == 0

    @classmethod
    def clear(cls):
        '''清空队列,只是把指针重置'''
        cls.ptr, cls.cur = 0, 0

    @classmethod
    def decode(cls, s):  # 例如 '2_T_3_-1'
        '''对获得的字符串解码转为数据并存储到队列'''
        s = s.split('_')
        for i, v in enumerate(s):
            cls.data[i] = int(v)
            # if ord(v[0]) > 70:  # letter
            #     cls.data[i] = True if v[0] == 'T' else False
            # else:
            #     cls.data[i] = int(v)
        cls.ptr = len(s)

    @classmethod
    def fillWithArray(cls, a, begin=2):
        cls.setAdding()
        for i in range(begin, len(a)):
            cls.add(a[i])

    @classmethod
    def encode(cls):
        '''对当前的队列内的数据编码，目前只涉及2种类型，数字与布尔值
        如果为空，返回空串，否则返回_以及数据，然后清空
        '''
        if cls.isEmpty():
            return ''
        for i in range(cls.cur, cls.ptr):
            cls.data[i] = str(cls.data[i])
        res = '_'+'_'.join(cls.data[cls.cur:cls.ptr])
        cls.clear()
        return res

    @classmethod
    def show(cls):
        if cls.isEmpty():
            testPrint('Queue is empty!')
            return
        for i in range(cls.cur, cls.ptr):
            testPrint(cls.data[i], end='_')
        testPrint('.')


DataStorage.init()

# print('ds init!')

#   res = ['']*cls.ptr
#   d = cls.data
#    for i in range(cls.ptr):
#         if isinstance(d[i], int):
#             res[i] = str(d[i])
#         else:  # isinstance(d[i],bool)
#             res[i] = 'T' if d[i] else 'F'
#     cls.clear()
#     return '_'.join(res)
