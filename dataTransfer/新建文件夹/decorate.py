

def decorate_1(func):
    def inner1(*args):
        print('1', func.__name__, args)
        func(*args)
    return inner1

def decorate_2(func):
    def inner2(*args):
        print('2', func.__name__, args)
        # if 1:
        #     print('不执行了！')
        #     return 
        func(*args)
    return inner2

class Test():
    def __init__(self) -> None:
        self.name='reimu'

    def before(fun):

        def inner(*arg):
            print('can')
            # res='marisa'
            return fun(*arg)
        '''
        注意两个函数之间变量不共通
        并且被修饰者返回的结果需要显式调用return 才能返回，不然就是不接收返回值的单纯调用
        '''
        return inner

    @before
    def getName(self):
        # return res
        return self.name

t=Test()
print(t.getName())


# @decorate_1
# @decorate_2
# # @beforeAsk
# def test(*args):
#     print('test', args)


# test(1,2,3,4,5,6)
# tmp = decorate_2(test)
# decorate_1(tmp)
# tmp(1,1,4,5,1,4)


# def beforeAsk(fun):
#     def inner(*arg):
#         if not Gui.ds.isEmpty():
#             return Gui.ds.get()
#         else:
#             fun(*arg)
#     return inner
