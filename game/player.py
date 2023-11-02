
# from .skill import Skill
from .GUI import Gui
import game.skill as skill
from .function import findHeadImage  #,findIndex
from .con_fun import whenOperateion,afterOperation
from .card import Card
from .dialog import messagebox
from .information import Info
from .netMessage import NetMessage
from dataTransfer.dataStorage import DataStorage as ds

from time import sleep
from random import shuffle,randint  # ,seed

speChar='_'

def recur(op:str):
    """ 重现操作的函数 """
    print('recurrent code',op)
    each = [int(v) for v in op.split('_')]

    # 先填充存储队列，再运行操作，以使取值有效
    a=each[0]
    ds.fillWithArray(each, 2)
    ds.setGetting()
    Player.cp.function[a](each[1])

    # if a<6:
    #     Player.cp.function[a](each[1])
    # else:
    #     Player.cp.function[a]()
    # ds.setNormal() 修饰函数会设置正常状态，所以不用在这里设定
        
class Player():
    
    now,total,first=0,0,0
    turnsCount = 1

    haveInit = False
    player: list["Player"] = []
    cp :"Player" = None

    resource  =[0,0,0]
    exResource=[0,0,0]
    used : list[Card] = []
    exile: list[Card] = []
    faithCard,faithChar=0,0
    cardTemp=None
    
    buffNames =['赛钱箱','丰聪耳神子','洋馆','圣白莲','依神紫苑',
        #   0         1          2       3      4 
        '依神女苑','神奈子的御柱','高丽野阿哞','八坂神奈子',
        # 5         6          7             8
        '纳兹琳','赛钱箱','宫古芳香','蕾米莉亚 斯卡雷特',None,'月之走廊']
        #9       10         11        12               13    14
    '''各个buff的名称,对应顺序就是索引'''
    buff  =[False]*15
    timing=[0]*5
    facilityState: list[bool] = []
    #       0        1    2      3    4
    #      before gain,retreat, exile,use                 
    #        4    4     3+1      2    1
    
    @staticmethod
    def recurAll(file):
        ds.setGetting()
        with open(file) as f:
            f.readline()
            f.readline()
            for line in f.readlines():
                recur(line[:-1])
                Gui.root.update()
                sleep(0.1)
        ds.setNormal()
                
    def __init__(self,no,name,photo):
        """ 编号以及名称、头像，初始卡组由外部添加 """
        self.deck:     list[Card] = []
        self.throw:    list[Card] = []
        self.hand :    list[Card] = []
        self.repeat:   list[Card] = []
        self.facility: list[Card] = []
        self.monster:  list[Card] = []
        self.monster2: list[Card] = []
        self.no=no
        self.name=name
        if photo==None:
            self.image=findHeadImage(no)
        else:self.image=photo

        self.guide=[
            self.monster2,
            self.monster,
            self.facility,
            self.hand,
            self.repeat,
            Player.used,
            self.deck,
            self.throw,
            ]
        self.function=[
            None,      
            self.gain, #从1开始...
            self.use,
            self.launch,
            self.catch,
            # Player.end, # 5
            Player.endAndNext, # 5
            Player.next, # 6
            skill.Skill.spellAny,    # 7
            ]
    
    @classmethod
    def clear(cls):
        '''游戏结束后进行清理工作'''
        for p in cls.player:
            # del p.image
            for i in range(7):
                 p.guide[i].clear()
        cls.player.clear()
        cls.exile.clear()
        cls.haveInit=False

    @classmethod
    def countScore(cls,empty):
        '''游戏结束后各玩家计分'''
        allCard=[]
        for p in cls.player:
            cardNum,score,library=0,0,False
            Gui.newMessage(f'-----{p.name}:')
            allCard=[p.monster2,p.monster,p.facility,p.hand,
                p.deck,p.throw,p.repeat]
            for i in p.monster:
                score+=i.score
            for i in p.monster2:
                score+=i.score
            for i in range(2,7):
                for j in allCard[i]:
                    if j!=None and j.place in empty:
                        score+=j.score
            cardNum = sum(len(i) for i in allCard)
            Gui.newMessage('score:',score)
            Gui.newMessage('Number of cards:',cardNum)
    
    def checkMiracle(name):
        '''翻牌后发生奇迹事件的处理'''
        Gui.newMessage(f'奇迹:{name}')
        skill.Skill.checkMiracle(name)
    
    @classmethod
    def exileAdd(cls,card):
        '''放逐某一张牌'''
        Gui.newMessage(f'放逐了{card.name}')
        if cls.timing[3] and cls.buff[14] and card.category()==0 and Player.cp.haveFacility('月之走廊'):
            # cls.timing[3]-=1
            # cls.buff[14]=False
            Player.resource[0]+=1
            Gui.showResource(cls.resource)
            cls.lostBuff(14)
        cls.exile.append(card)
    
    @classmethod
    def appendBuff(cls,name):
        '''添加buff'''
        i=Player.buffNames.index(name)
        Player.buff[i]=True
        if i==0:
            Player.buff[10]=True
            Player.timing[2]+=1
        Player.timing[(i-2)//4]+=1
        Gui.tip.append(i)
        Gui.newMessage(f'获得增益：{name}')
    
    @classmethod
    def lostBuff(cls,i):#,cut=True
        '''失去buff'''
        if not Player.buff[i]:return
        Player.buff[i]=False
        Player.timing[(i-2)//4] = max(Player.timing[(i-2)//4]-1,0)
        Gui.tip.lost(i)
        Gui.newMessage(f'失去增益：{Player.buffNames[i]}')
    
    @classmethod
    def exileOneP(cls):
        '''当前玩家放逐'''
        return cls.cp.exileOne()
    
    @classmethod
    def init(cls,name:str,photo,without):
        '''初始化所有玩家，使用字符串，以及Image对象而不是头像文件名称'''
        cls.player: list[Player] = []
        # 如果没有设置则使用默认配置
        n=len(name)
        if without==None:
            n=3
            without=[randint(0,2) for i in range(n)]
            photo=[None]*n
            name=['灵梦','魔理沙','爱丽丝','早苗'] #'神绮','摩多罗','幽香',

        # 初始卡牌创建
        init=['',[[]],10,0]
        rice = Card('仆役',[0,0,0],[0,0,1],*init,2)  #★','◎','♨
        money= Card('茶商',[0,0,0],[0,1,0],*init,1)
        faith= Card('信徒',[0,0,0],[1,0,0],*init,0)
        c=[[faith]*5,[money]*5,[rice]*5]

        # 给每位玩家分配初始卡牌
        for i in range(n):#i代表第几位玩家
            cls.player.append( Player(i,name[i],photo[i]) )
            for x in range(3):#x代表第几位资源
                if x!=without[i]:
                    cls.player[i].deck+=c[x]
            shuffle(cls.player[i].deck)
            cls.player[i].draw(5,False)
            
        # public lists initialize，对公用内存的初始化
        cls.haveInit=True
        cls.turnsCount = 0
        cls.total = n
        cls.first = randint(0, n-1)
        cls.now = cls.first-1
        cls.nextAdd()
        ds.setGetting()
        cls.next()

        ds.setGetting()
        Gui.newMessage(f'从{cls.player[cls.first].name}开始.')
        Gui.other.newPlayer(name, without, cls.first)
        Gui.checkMiracle()
        ds.setNormal()

    @classmethod
    def nextAdd(cls):
        cls.now += 1
        if(cls.now == cls.total):
            cls.now = 0
        Info.currentPlayer = cls.now

    @classmethod
    @whenOperateion
    def next(cls,*e):
        '''下一位玩家'''
        # 相关变量设置
        print('Next player:',flush=True)
        NetMessage.instance.add('6_0')
        if(cls.now == cls.first):
            cls.turnsCount += 1
            Gui.newMessage(f'----第{cls.turnsCount}轮：')  # player
            if Gui.isGameOver(Player.total):
                Gui.newMessage('游戏结束!')
                empty = Gui.askEmpty()
                Player.countScore(empty)
                return

        # 记录,列表清空
        cls.used.clear()
        cls.facilityState.clear()
        for i,_ in enumerate(cls.buff):
            cls.buff[i]=False
        for i, _ in enumerate(cls.timing):
            cls.timing[i]=0
        # for i in range(3):
        #     cls.resource[i],cls.exResource[i]=0,0ss

        # 新玩家资源计算
        cls.faithChar = cls.faithCard = 0
        cls.cp: Player = cls.player[cls.now]
        p=cls.cp
        Gui.newMessage(f'----{p.name}的回合：')# player 
        p.gainFromFacility()
        p.gainFromMonster()

        # check begin,restraint,repeat
        Gui.flash(p) #include hand,facility,monster
        for n, i in enumerate(p.hand):
            if i==None:continue
            if i.canRestraint(): #'克制'
                if messagebox.askyesno('克制',f'是否丢弃{i.name},然后抽一张卡？'):
                    p.throwAnddraw(n)
        p.repeatCard()
    
    @classmethod
    # @whenOperateion
    def endAndNext(cls,*args):
        """ 因为end不能调用next，所以这么写，实际上目前end不会涉及任何操作数据 """
        # NetMessage.instance.add('5_0')
        cls.end()
        cls.nextAdd()

        if Info.isCurrent():
            ds.clear()
            ds.setAdding()
            print('Current player:', flush=True)
            cls.next()
        else:
            print('Not current player:', flush=True)
        # return '5_0'
    
    @whenOperateion
    def end(*e):
        '''结束回合,处理迂返卡牌,手上未使用卡牌,检查结束阶段的效果'''
        p=Player.cp
        NetMessage.instance.add('5_0')
        for i in Player.used:
            if i.canReappear():  # 迂返
                p.repeat.append(i)
            else:
                p.throw.append(i)
        for i in p.hand:
            if(i!=None):p.throw.append(i)
        p.hand.clear()
        p.draw(5,False)
        skill.Skill.checkEnd()
        # return '5_0'

    @classmethod
    def drawP(cls, n=1):
        '''当前玩家抽一张'''
        cls.cp.draw(n)
    
    def throwAnddraw(self,n):
        '''丢弃第n张牌，并抽一张。用于克制'''
        self.lost(n)
        self.draw()

    def gainFromFacility(self):
        '''回合开始时,添加设施的buff,计算所有设施提供的资源量'''
        for i in range(3):
            self.resource[i]=0
        for i in self.facility:
            if i.hasBuff(): #check buff
                Player.appendBuff(i.name)
            for j in range(3): #gain
                Player.resource[j]+=i.gain[j]
            self.facilityState.append(i.canBeClick())
        Gui.showResource(Player.resource)
    
    def gainFromMonster(self):
        '''回合开始时,计算所有妖怪提供的备用资源量'''
        for i in range(3):
            self.exResource[i] = 0
        for i in self.monster:
            r=i.skill[0]
            for j in r:
                if j<3:Player.exResource[j]+=1
        Gui.showexResource()
    
    def launchOne(event):
        '''显示所有设施,并可以选择一张发动效果'''
        p=Player.cp
        ask=Gui.askOne2(p.facility,p.name,'选择一张发动:')
        if ask==-2:return
        Player.cp.launch(ask)
    
    def useAll(*event):
        '''从右到左使用所有手牌,所以会忽略使用完后抽的牌'''
        if (not Player.haveInit) or (not Info.isCurrent()):
            return 
        p=Player.cp
        n=len(p.hand)            
        for i in range(n):
            if n-i-1>=len(p.hand):break
            if(p.hand[n-i-1]!=None):p.use(n-i-1)
    
    def launchAll(*event):
        '''从前往后发动所有设施,目前不用'''
        p = Player.cp
        for i, _ in enumerate(p.facility):
            p.launch(i)
            
    def checkDeck(self) ->bool:
        '''检查卡组以及弃牌堆是否满足有一张卡可抽,满足时返回False,否则True'''
        if self.deck==[]:
            Gui.newMessage(f'{self.name}洗牌.')
            self.deck,self.throw=self.throw,[]
            if(self.deck==[]):
                Gui.newMessage('已无卡可抽!')
                return True
            shuffle(self.deck)
            Gui.showShuffle(len(self.deck))
        return False
    
    def draw(self,n=1,show=True):
        '''抽n张牌,show参数代表是否要在界面上刷新'''
        for i in range(n):
            if self.checkDeck():
                n-=i
                break
            card=self.deck.pop()
            if card!=None:self.hand.append(card)
            else:
                n-=1
                continue
            if(show):Gui.handAppend()
        Gui.newMessage(f'{self.name}抽了{n}张牌')
    
    def gainResourse(self,card):
        '''获取使用的牌card的资源'''
        if any(card.gain):
            for i in range(3):
                Player.resource[i]+=card.gain[i]
            Gui.showResource(Player.resource)    
        
    def canGain(self,card):
        '''判断当前资源能否获得card,对于人里的牌不在这里判断'''
        if card.place==10 :return True
        if card.name!='博丽灵梦':
            return skill.Skill.checkBeforeGain(card)
        else:
            return Player.resource[0]+Player.resource[1]>5

    def cost(self,card,no):
        '''消耗资源获取卡牌，返回True代表没有获取'''
        if card.place!=10:
            if card.name!='博丽灵梦':
                for i in range(3):
                    Player.resource[i]-=card.cost[i]
            else:
                res=Player.resource
                n=Gui.askANumber(res[0],
                    '博丽灵梦','选择要消耗的信仰数量：')
                money=6-n
                if money<=res[1]:
                    res[0]-=n
                    res[1]-=money
                else:
                    Gui.newMessage('请消耗总共6点资源！')
                    return False
        else: #人里
            if self.gainPeople(card):return False
        self.obtain(card,no)
        return True
 
    def gainPeople(self,people):
        '''人间之里牌的判断与消耗都在这里处理,若果返回True代表资源不足或者取消获得'''
        moreThan3=[]
        for i in range(3):
            if(Player.resource[i]>2):
                moreThan3.append(i)
        length=len(moreThan3)
        if(length==0):return True 
        elif(length==1):
            theType=moreThan3[0]
        else:
            theType=Gui.askAType(moreThan3,'获得人间之里升级牌'
                ,'选择要消耗的资源：')
        if(theType==None):return True
        Player.resource[theType]-=3
    
    def obtain(self, card: Card, no=10):
        '''获得中央牌堆的卡牌,或者退治妖怪，然后翻开下一张'''
        Gui.showResource(Player.resource)  # 为什么在这里show呢(
        if card.category() == 2:  # monster
            Gui.newMessage(f'{self.name}退治了{card.name}.')
            self.gainResourse(card)
            skill.Skill.retreatSkill(card)
            if(card.canBeClick()):
                self.monster.append(card)
                Gui.monsterAppend()
            else:
                self.monster2.append(card)
            skill.Skill.checkRetreat(card.totalCost())
            self.gainFromMonster()
        else:  # character or facility
            Gui.newMessage(f'{self.name}获得了{card.name}.')
            if self.checkGaining(card):
                self.throw.append(card)
        Gui.nextCenter(no)

    @whenOperateion
    def gain(self,no):
        '''获取中央某一card的流程,判断后再消耗资源'''
        card=Gui.getCover(no)
        NetMessage.instance.add(f'1_{no}')
        if(self.canGain(card)):
            if not self.cost(card,no):return False
            # return f'1_{no}'
        else:
            Gui.newMessage('资源不足!')
            return False
        
    @whenOperateion
    def use(self,no):
        '''使用一张手牌'''
        # print('player using:',flush=True)
        card:Card=self.hand[no]
        c=card.category()
        had=False
        NetMessage.instance.add(f'2_{no}')

        Gui.newMessage(f'使用了{card.name}')
        self.hand[no]=None
        Gui.handLost(no)

        if c==0:#角色
            skill.Skill.spell(card)
            if skill.Skill.card!=None:
                Player.used.append(card)
        else:#设施
            if self.haveFacility(card.name):
                Gui.newMessage('已拥有。')
                self.draw()
                had=True
                Player.used.append(card)
            if(not had):
                if card.hasBuff(): #check buff
                    Player.appendBuff(card.name)
                self.facilityAppend(card)
        if(not had):
            self.checkUsing(card)
            self.gainResourse(card)
        # return f'2_{no}'

    @whenOperateion
    def launch(self, no):
        '''发动某一设施的效果,注意有自毁效果，所以需要判断下'''
        if not self.facilityState[no]:
            return
        card = self.facility[no]
        Gui.newMessage(f'发动了{card.name}')
        NetMessage.instance.add(f'3_{no}')
        r = skill.Skill.spell(card)
        if not r:  #发动设施后，记录与后处理
            if no>=len(self.facility) or  card.name!=self.facility[no].name:
                return
            self.facilityState[no] = False
            if no>7:return
            Gui.facilityLaunch(no)
            # return f'3_{no}'
        else:
            return False
    
    @whenOperateion
    def catch(self,no):
        '''捕获一个妖怪'''
        if no>=len(self.monster):return
        m=self.monster[no]
        Gui.newMessage(f'{self.name}捕获了{m.name}')
        r=skill.Skill.spell(m)
        NetMessage.instance.add(f'4_{no}')
        
        #return None or 0 will catch it,but 1 represent mistake
        if not r:
            Player.exileAdd(self.monster.pop(no))
            self.gainFromMonster()
            Gui.monsterLost(no)
            # return f'4_{no}'
        else:
            return False

    
    def showDeck(self):
        '''将卡组按照类型与数量展示(顺序打乱)'''
        m={}
        for i in self.deck:
            m[i.name]=m.get(i.name,0)+1
        res = [(m[i], i) for i in m]
        res.sort(reverse=True)
        text = f"{self.name}的卡组:\n"
        for (i, j) in res:
            text += f'{j}x{i}\n'
        text=text[:-1]
        Gui.newMessage(text)
    
    def lost(self,no):
        '''丢弃一张手牌进入弃牌堆'''
        card=self.hand[no]
        self.hand[no]=None
        self.throw.append(card)
        # if card!=None:self.throw.append(card)
        # else:print('---------------丢弃时出错')
        Gui.newMessage(f'{self.name}丢弃了{card.name}.')
        Gui.handLost(no)
    
    def repeatCard(self):
        '''迂回生效处理'''
        if(self.repeat==[]):return
        for card in self.repeat:
            Gui.newMessage('迂返生效:'+card.name)
            self.gainResourse(card)
            skill.Skill.spell(card)
            self.throw.append(card)
        self.repeat.clear()  
    
    def exileOne(self):
        '''放逐一张牌'''
        #只删除弃牌堆与手卡的0或1分卡,
        #并且当弃牌堆与手卡有同名的卡时,只能删除弃牌堆的
        card,no,name=[],[],set()
        inThrow=0
        # 整理弃牌堆的
        for n, i in enumerate(self.throw):
            if(i.score<2 and (i.name not in name)):
                inThrow+=1
                card.append(i)
                no.append(n)
                name.add(i.name)
        # 整理手上的
        for n, i in enumerate(self.hand):
            if(i==None):continue
            if(i.score<2 and (i.name not in name)):
                card.append(i)
                no.append(n)
                name.add(i.name)

        if(no==[]):
            Gui.newMessage('无卡可放逐!') #No card can be exiled
            return 0

        r=Gui.askOne(card,inThrow,no,self.name)
        if(r==-2):#不放逐
            Gui.newMessage('取消放逐.')
            return -2
        else:
            index=no[r]
            if(r<inThrow): #throw
                self.throw.pop(index)
            else: #hand
                self.hand[index]=None
                Gui.handLost(index)
            # Gui.newMessage(f'{self.name}放逐了{name[r]}')
            Player.exileAdd(card[r])
    
    def facilityAppend(self,card:Card):
        self.facility.append(card)
        self.facilityState.append(card.canBeClick())
        Gui.facilityAppend()
        
    def destory(self,no,show=True):
        '''摧毁一座设施'''
        if(no>=len(self.facility)):
            Gui.newMessage('越界!')#Out of index
            return 1
        f = self.facility.pop(no)
        self.facilityState.pop(no)
        self.throw.append(f)
        name=f.name
        if show:
            Gui.facilityLost(no)
            for i,v in enumerate(Player.buffNames):
                if v==name:Player.lostBuff(i)
        Gui.newMessage(f'摧毁了{self.name}的{name}.')
    
    def selfDestory(self,name):
        '''自己摧毁自己的特定设施'''
        for n, i in enumerate(self.facility):
            if i.name==name :
                self.destory(n)
                return
        Gui.newMessage(f'找不到{name}!')#Can not find 
        return 1
    
    def haveFacility(self,name):
        '''玩家是否具有特定设施'''
        for i in self.facility:
            if(i.name==name):return True
        return False
    
    def checkUsing(self,card:Card):
        '''使用手牌时触发的buff流程'''
        if(card.isFaith()):#信仰相关记录
            Player.faithCard+=1
            if(card.category()==0):
                Player.faithChar+=1
                if (Player.buff[0] 
                    and Player.faithChar==1 
                    and self.haveFacility('赛钱箱')):
                    Gui.newMessage('赛钱箱生效。')
                    Player.lostBuff(0)
                    Player.resource[1]+=1
                    Gui.showResource(Player.resource) #'赛钱箱'
        if( Player.buff[1] and card.place==10):
            # print('miko')
            cnt=0
            for i in Player.used:#'丰聪耳神子'
                if(i.name==card.name):cnt+=1
            if cnt>1:return
            self.gainResourse(card)
            Gui.newMessage('丰聪耳神子生效。')
    
    def checkGaining(self,card):
        '''获得手牌(目前仅限信仰牌)时触发的效果,若果卡牌不是正常进入弃牌堆，返回False'''
        if (not Player.timing[1]) or (not card.isFaith()):
            return True
        b=Player.buff
        name=card.name
        c=card.category()
        if b[9] and c==1:
            Gui.newMessage('纳兹琳生效。')
            ask=messagebox.askyesno('纳兹琳',
                        f'是否将{name}加入手卡？')
            if ask:
                self.hand.append(card)
                Gui.handAppend()
                Player.lostBuff(9)
                return False
        #if go to other place,return false
        result=True
        for i in range(6,9):
            if b[i]:#如果有buff
                if i<8:#御柱,阿牟
                    if i==6 and not self.haveFacility('神奈子的御柱'):
                            continue
                    Gui.newMessage(f'{Player.buffNames[i]}生效。')
                    ask=messagebox.askyesno(Player.buffNames[i],
                        f'是否将{name}放置在牌堆顶？')
                    if ask:
                        self.deck.append(card)
                        result= False
                        break
                        #Player.cardTemp=None
                else:#八坂神奈子
                    Gui.newMessage('八坂神奈子生效。')
                    ask=messagebox.askyesno('八坂神奈子',
                        f'是否将{name}加入手卡？')
                    if ask:
                        self.hand.append(card)
                        Gui.handAppend()
                        result= False
                        break
        for i in range(6,9):
            if b[i]:Player.lostBuff(i)
        return result

    def handNumber(self):
        '''计算手牌数量'''
        n=0
        for i in self.hand:
            if i != None:n+=1
        return n
    
    def rebuild(self):
        '''从弃牌堆选一张设施加入手牌'''
        card,no,n=[],[],-1
        for i in self.throw:
            n+=1
            if(i.category()==1):
                card.append(i)
                no.append(n)
        if(card==[]):
            Gui.newMessage('没有设施牌在弃牌堆!') #No facility in throw
            return 1
        elif len(no)==1:
            r=0
        else:#
            r=Gui.askOne2(card,'选择一张重建')
            if (r==-2) :return 1
        #上手
        self.hand.append(card[r])
        self.throw.pop(no[r])
        Gui.handAppend()
        Gui.newMessage(f'{self.name}重建了{card[r].name}.')
    
    def neatHand(self):
        '''整理手牌,将None全部去除'''
        # self.hand=[i for i in self.hand if i!=None]
        n=0
        for i in self.hand:
            if i==None:n+=1
        for i in range(n):self.hand.remove(None)
    
    def bind():
        # 给界面绑定快捷键，初始化Skill类
        skill.Skill.init()
        Gui.showHome()
        Gui.root.bind('<space>', Player.useAll)
        Gui.root.bind('<Control-f>', Player.launchOne)

        Gui.root.bind('<Control-e>', Gui.end)
        Gui.root.bind('<Control-r>', Gui.returnHome)
        Gui.root.bind('<Control-q>', Gui.beNormal)
        Gui.root.bind('<Control-t>', Gui.changeAlpha)
        # Gui.root.bind('<Control-p>', Gui.setSeed)
        # Gui.root.bind('<Control-u>', Gui.askRecur)

        Gui.root.bind('<Control-s>', skill.Skill.spellAny)
        Gui.root.bind('<Control-m>', lambda a: skill.Skill.checkMiracle('神奈子的御柱') )
        # Gui.root.bind('<Control-g>', skill.Skill.gainAnyCard)
        # Gui.root.bind('<Control-d>', ds.init)

    @classmethod
    def endAndNext2(cls, *args):
        """ 因为end不能调用next，所以这么写 """
        # 如果能够取值，代表正在重复，直接本地运行一遍，不传递操作
        ni = NetMessage.instance
        if ds.canGet():
            ds.setNormal()
        else:
            ni.setHead('2_')
            ds.setAdding()
            NetMessage.instance.add('5_0')

        cls.end()
        if Info.isCurrent():
            ds.clear()
            ds.setAdding()
            cls.next()
        else:
            afterOperation(ni.getMessage())

    # def checkBeforeGaining(self):
    #     '''交由Skill完成,上面几个check理论上也应当由Skill完成比较好?'''
    #     pass
    # def showThrow(self):
    #     name=[]
    #     for i in self.throw:
    #         name.append(i.name)
    #     Gui.newMessage(self.name,'的弃牌堆:',name)

    # def showHand(self):
    #     name=[]
    #     for i in self.hand:
    #         if i==None:name.append('None')
    #         else:name.append(i.name)
    #     Gui.newMessage(self.name,'的手牌:',name)
    # def count(self):
    #     #计算储备资源
    #     listsAdd(Player.exResource,self.monster)
    #     self.gainResourse(self.facility)



# Gui.init()
# print(time()-timeCount)
# Gui.root.mainloop()
# def listsAdd(a,b):#a is resourse,b are cards
#     for i in b:
#         for j in range(3):a[j]+=i.gain[j]
