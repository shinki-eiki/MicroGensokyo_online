
# class DataStorage:
#     '''用一个大数组模拟的队列，该队列在某次操作中只能添加或者只能获取数据，'''
    
    
#     def __init__(cls) -> None:
#         '''original length is 100. '''
#         cls.data=[None]*100
#         cls.cur=0 
#         #队列头部指针，这里指向的是当前头部元素（未取），队列为空时
#         cls.ptr=0 #下一个插入的位置，即队列尾的下一个
#         cls.state=0 
#         #队列是否正在添加，1代表正在添加，此时不能取值

#     def setAdding(cls):
#         '''Set the state to be true.We cann't get value from it. '''
#         cls.state = 1

#     def cancelAdding(cls):
#         '''Set the state to be false.We can get value from it. '''
#         cls.state=0    
        
#     def add(cls,val):
#         '''向队列中添加一个值，'''
#         if cls.ptr>=len(cls.data):
#             cls.data+=[None]*10
#         if isinstance(val,bool):
#             cls.data[cls.ptr] = int(val)
#         else:
#             cls.data[cls.ptr] = val
#         cls.ptr += 1

#     def get(cls):
#         '''获取头部值'''
#         if not cls.canGetVal():
#             testPrint('Can not get!')
#             return -114
#         res=cls.data[cls.cur]
#         cls.cur+=1
#         if cls.cur==cls.ptr:
#             cls.clear()
#         return res
    
#     def getAll(cls):
#         '''获取所有值，然后清空'''
#         res=cls.data[:cls.ptr]
#         cls.clear()
#         return res
    
#     def canGetVal(cls):
#         '''队列能否取值,要求不是正在添加且不为空'''
#         return not (cls.state or cls.isEmpty())
    
#     def isEmpty(cls):
#         '''队列是否为空'''
#         return cls.ptr==0
    
#     def clear(cls):
#         '''清空队列,只是把指针重置'''
#         cls.ptr,cls.cur=0,0
        
#     def decode(cls, s):  # 例如 '2_T_3_-1'
#         '''对获得的字符串解码转为数据并存储到队列'''
#         s = s.split('_')
#         for i, v in enumerate(s):
#             if ord(v[0]) > 70:  # letter
#                 cls.data[i] = True if v[0] == 'T' else False
#             else:
#                 cls.data[i] = int(v)
#         cls.ptr = len(s)

#     def encode(cls):
#         '''对当前的队列内的数据编码，目前只涉及2种类型，数字与布尔值'''

#         return '_'.join(cls.data[cls.cur:cls.ptr])

#         res = ['']*cls.ptr
#         d = cls.data
#         for i in range(cls.ptr):
#             if isinstance(d[i], int):
#                 res[i] = str(d[i])
#             else:  # isinstance(d[i],bool)
#                 res[i] = 'T' if d[i] else 'F'
#         cls.clear()
#         return '_'.join(res)

#     def show(cls):
#         if cls.isEmpty():
#             testPrint('Queue is empty!')
#             return
#         for i in range(cls.cur,cls.ptr):
#             testPrint(cls.data[i],end='_')
#         testPrint('.')
