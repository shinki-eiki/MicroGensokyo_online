
import random
import randTest2

if __name__=='__main__':

    random.seed(114)
    for i in range(3):
        randTest2.fun()
        print()
    # for i in range(1):
    #     print(random.randint(1,10),end=',')
    #     a=[i for i in range(10)]
    #     random.shuffle(a)
    #     print(a)

    # random.seed(114)
    for i in range(10):
        print(random.randint(1, 10), end=',')
        # a = [i for i in range(10)]
        # random.shuffle(a)
        # print(a)
