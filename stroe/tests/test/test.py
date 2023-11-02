

# import random
# random.seed(114514)
# ---readlines会受到先前读取的影响
# with open('2-12.log') as f:
#     f.readline()
#     f.readline()
#     for line in f.readlines():
#         print(line[:-1])
        
# # find matched item in a list
# # num = [i for i in range(10) if i & 1 == 1]

# testPrint=None
# def fun2(*a):
#     # print(type(a))
#     # print(a)
#     for i in a:print(i)
# def fun(*a):
#     fun2(*a)
# fun(1,2,3)
# def fun1():
#     import function
#     # print(type(testPrint))
#     return function

# def fun2(p):
#     p.testPrint('yes')

# print(type(testPrint))
# pack=fun1()
# print(type(pack))
# fun2(pack)
# print(type(testPrint))

#next filter() will return a genarator but list
# lst = [i for i in range(10)]
# lst2 = [i for i in range(10)]
# # 有列表a，令b=a，再令a指向一个新列表，那么b仍指向旧列表
# tl=lst
# print(id(lst),id(tl))
# # lst.clear()
# lst=[1]
# # lst=lst[:2]
# print(tl)
# print(id(lst), id(tl))

# num=filter(lambda a:a&1==0,lst)
# for i in num:
#     print(i)
# print(num)

# #map() can process two or more value
# def add(a,b):
#     return a+b

# print(map(add,lst,lst2))

# for i in range(100):
#     if i==100:break
# else:
#     print('finish')
#     print(random.randint(0,100),end=',')

# from package.test1 import fun
# from package.test import fun

# from package.test1 import test
# from package import test

# test.fun()
