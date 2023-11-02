'''
测试读取中文的卡片data
'''

from json import loads
from game.card import Card

def readData(df='cardData.dat'):
        file=open(df,'r',encoding='utf-8')
        n,order=0,0
        cc=[[] for i in range(12)]
        cn=[[] for i in range(12)]
        res=''
        for j in file.readlines():
            if(j=='next place:\n'):
                n+=1
                # if n==1:break
                order=0
                res += 'next place:\n'
                continue
            i=loads(j)
            # print(i,end='%')
            # print(str(i))
            print(type(i))
            res += str(i)+'%'
            typeNum=i[8]
            num=i[7]
            i=i[0:-2]
            i.append(order)
            cn[n].append(num)
            order+=1
        file.close()
        with open('temp.dat',mode='w',encoding='utf-8') as f:
            f.write(res)

for i in range(3):
    print('=====================')
# readData()

Card.readData('temp.dat')
cc: list[list[Card]] = Card.card
print(cc[2][4].text)
