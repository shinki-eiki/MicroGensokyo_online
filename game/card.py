

from .function import findCardImage
# from function import findCardImage
from json import loads
from random import shuffle

class Card():
    """All the data of a card."""
    #image=findImage()
    colors=['green','purple','yellow','red',
        'blue','pink','lightgrey','silver','orangered','lightgreen',]
    typeList=['角色','设施','妖怪']
    gainText=['   ','每回合','奖励:']
    char=['★','◎','♨']
    placeName=['守矢神社','命莲寺','神灵庙','博丽神社',
    '永远亭','白玉楼','魔法之森','地灵殿','红魔馆','兽道','人间之里']
    
    def __init__(self,name,cost,gain,text,skill,place,score,no):
        self.name =name
        #self.num  =num
        self.cost = cost
        self.gain = gain
        self.text = text
        self.special = 0
        # if len(skill) != 0 and isinstance(skill[-1],int):
        #     self.special = skill.pop()
        self.skill = skill
        self.score=score
        self.place=place
        self.no=no
        self.allText= None
        self.handText=None
        # n,no=len(text),0
        # while n>=14:
        #     self.text+=text[14*(no):(no+1)*14]+'\n'
        #     n-=14
        #     no+=1
        # self.text+=text[no*14:]+'\n'
        self.image=None   
        
    def getImage(self):
        # return Card.image
        if self.image==None:
            guide=str(self.place)+str(self.no)
            self.image=findCardImage(guide)
        return self.image

    def createImage():
        # Card.image=findCardImage('cover') 
        Card.image=findCardImage('test') 

    def __repr__(self):
        return self.name

    def __str__(self):
        if self.allText==None:
            cost,gain,cardType='','',''
            for i in range(3):
                cost+=Card.char[i]*self.cost[i]
                gain+=Card.char[i]*self.gain[i]
            if(self.isFaith()):cardType+='信仰'
            else:cardType+='中立'
            c=self.category()
            cardType+=Card.typeList[c]
            if(gain!=''):
                gain='   '+Card.gainText[c]+gain       
            p=Card.placeName[self.place]
            self.allText='%s\n\
%s\n\
%12s%8d\n\
%13s\n\
%s\n\n\
%21s\n '%(self.name,cost,cardType,self.score,gain,self.text,p)

#f'{self.name}\n\
# \t{cost}\n\
# \t\t{cardType}\t   {self.score}\n\
# \n\t\t{gain}\n\
# {self.text}\n\n\
# \t\t\t\t\t\t{p}\n\\n'
        return self.allText
        
    def inCenter(self):
        cText=''
        for i in range(3):
            cText+=Card.char[i]*self.cost[i]
        return f'{self.name}\n{cText}'
    
    def inHand(self):
        if self.handText==None:
            self.handText=self.name+'\n'
            for i in range(3):
                self.handText+=Card.char[i]*self.gain[i]
        return self.handText
    
    def category(self):return 0
    #0:character 1:facility 2:monster
    
    def totalCost(self):
        return sum(self.cost)

    def isFaith(self):
        return bool(self.cost[0])

    def canBeClick(self)->bool:
        return self.skill[0]!=[]

    def readData(df='cardData.dat'):
        file=open(df,'r',encoding='utf-8')
        n,order=0,0
        cc=Card.card= [[] for i in range(12)]
        cn=Card.num = [[] for i in range(12)]
        for j in file.readlines():
            if j=='End\n':break
            if(j=='next place:\n'):
                n+=1
                order=0
                continue
                # break
            i=loads(j)
            typeNum=i[8]
            num=i[7]
            i=i[0:-2]
            i.append(order)
            if  (typeNum==0):  c=Character(*i)
            elif(typeNum==1):  c=Facility(*i)
            else :             c=Monster(*i)
            cc[n].append(c)
            cn[n].append(num)
            order+=1
        file.close()
        init=['',[[]],10,1]
        rice =Card('佣人',  [0,0,0],[0,0,2],*init,5)
        money=Card('烧具商',[0,0,0],[0,2,0],*init,4)
        faith=Card('教徒',  [0,0,0],[2,0,0],*init,3)
        card=[faith,money,rice]
        for i in range(3):#人里卡牌初始化
            cc[10].append(card[i])

    def newCenter(center,exceptOne):
        for i in range(len(Card.card)):
            if i!=exceptOne:
                if i==10:break
                for j in range(len(Card.card[i])):
                    one=[Card.card[i][j] for k in range(Card.num[i][j])]
                    center[i]+=one
                shuffle(center[i])
        for i in range(3):#人里卡牌初始化
            center[10+i].append(Card.card[10][i])
        center.pop(exceptOne)

    @classmethod
    def gainAnyCard(cls,place,no):
        return cls.card[place][no]

    # len(self.skill)!=0 and self.skill[-1]==5
    def hasBuff(self):      return 1 in self.skill #self.special==1
    def canReappear(self):  return 3 in self.skill #self.special == 3
    def canRestraint(self): return 4 in self.skill #self.special == 4
    def hasMiracle(self):   return 5 in self.skill #self.special == 5

class Character(Card):
    #"""docstring for Monster"Card      
    def __init__(self,name,cost,gain,text,skill,place,score,no):
        Card.__init__(self,name,cost,gain,text,skill,place,score,no)

class Facility(Card):
    #"""docstring for FacilityCard
    def __init__(self, name,cost,gain,text,skill,place,score,no):
        Card.__init__(self,name,cost,gain,text,skill,place,score,no)

    def category(self):return 1
    
class Monster(Card):
    #"""docstring for Monster"Card      
    def __init__(self,name,cost,gain,text,skill,place,score,no):
        Card.__init__(self,name,cost,gain,text,skill,place,score,no)
        
    def category(self):return 2

if __name__ == "__main__":
    def toSQL():
        import pymysql
        con=pymysql.connect(host='localhost',user='root',password='123456',db='javabook')
        cur=con.cursor()
        sql='insert into mg (id,`name`,place,type,score,num,\
        cost0,cost1,cost2,gain0,gain1,gain2) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        #
        Card.readData()
        c=Card.card
        id=0
        try:
            for i in c:
                for j in i:
                    cur.execute(sql,(id,j.name,j.place,j.category(),\
                        j.score,1,j.cost[0],j.cost[1],j.cost[2],\
                        j.gain[0],j.gain[1],j.gain[2]))
                    id+=1
            con.commit()
        except  Exception as e:
            print('Exception!!!')
            print(e)
            con.rollback()
        finally:
            # print()
            con.close()
            cur.close()

    Card.readData('cardData.dat')
    cc:list[list[Card]]=Card.card
    print(cc[2][4].text)
    # cn=Card.num
    # res=[0,0,0]
    # total=[0,0,0]
   
    # # print(len(c))
    # for i in range(10):
    #     print(Card.placeName[i],end=':')#
    #     for j in range(len(c[i])):
    #         # print(j.no,end=' ')
    #         for k in range(3):
    #             res[k]+=c[i][j].cost[k]*cn[i][j]
    #     print(res)
    #     for i in range(3):total[i]+=res[i] 
    #     res=[0,0,0]
    #     # n+=1
    # print(total)

