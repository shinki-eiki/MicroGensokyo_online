
import random

def fun():
    for i in range(10):
        print(random.randint(1,10),end=',')
    # random.seed(114)

if __name__ == '__main__':
    random.seed(514)

    for i in range(10):
        print(random.randint(1, 10), end=',')
        a = [i for i in range(10)]
        random.shuffle(a)
        print(a)

