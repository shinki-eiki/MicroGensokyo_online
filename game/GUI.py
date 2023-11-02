
from .card import Card
from .playerButton import PlayerButton
from .cardButton import CardButton
# from .choose import Choose
from .function import *
from .dialog import simpledialog, messagebox
from .information import Info
from .netUI.roomPage import RoomPage
# from .con_fun import whenAsk
from dataTransfer.dataStorage import DataStorage as ds

from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Notebook  #,Treeview,Combobox
from random import randint,seed   # ,shuffle
from time import sleep  # time,

def whenAsk(fun):
    '''在等待玩家操作前，确认是否已有值待取'''
    # return fun
    def inner(*arg, **kw):
        '''return fun(*arg) if Gui.ds.isEmpty() else Gui.ds.get()'''
        res = 0
        if ds.hasVal(): #能取值，就直接获取
            # sleep(0)
            res = ds.get()
        else:  # 不能取值，就走流程询问，并存储
            # ds.setAdding()
            res = fun(*arg, **kw)
            ds.add(res)
            # ds.setNormal()
        Gui.setTip()
        return res
    return inner

def whenClickOn(fun):
    """ 为了防止非当前玩家误触，在点击按钮前判断 """
    def inner(*args,**kw):
        # print('click',Info.currentPlayer,Info.thisPlayer)
        if Gui.isSpecial or not Info.isCurrent():
            print('Not current player!',flush=True)
            return
        # self=args[0]
        res = fun(*args,**kw)
        Gui.setTip('')
        return res
    return inner
# Player =game.player.Player

class Basic():
    '''包括控件的鼠标悬停事件绑定,新玩家的更新操作'''
    #explain,show,showText
    def __init__(self):
        '''初始化card列表，给自己的button绑定解释触发，所以要先初始化自己的button'''
        self.card:list[Card]=[]
        for i in self.button:
            i.bind('<Enter>',self.explain)
    
    def explain(self,event):
        '''绑定解释事件，鼠标悬停时触发'''
        index=event.widget['value']
        c=self.card
        if(index>=len(c)):return
        Gui.explain(c[index])
        
    def show(self,cards,reset=True):
        '''新玩家回合,更新区域内的控件'''
        self.card=cards
        n=len(self.card)
        if(n>8):n=8
        for i in range(n):
            self.ableOne(i)
        for i in range(n, 8):
            self.disbaleOne(i)

    def append(self):
        '''设置新控件的文本'''
        n=len(self.card)-1
        if(n>7):return
        self.ableOne(n)

    def showText(self,i):
        '''返回每个控件应该显示的文本'''
        if (self.card==[]):return ''
        return self.card[i].name
    
    def disbaleOne(self,i):
        '''将控件设为不可用'''
        self.text[i].set('')
        self.button[i].config(bg='grey')
        self.button[i]['state'] = 'disable'
    
    def ableOne(self,i):
        '''将控件设为可用'''
        self.text[i].set(self.showText(i))
        self.button[i]['state'] = 'normal'
        
class Other():
    '''最右的边框，显示游戏记录以及玩家信息，以及弃牌堆和卡组数量'''
    place=('一般怪兽区','可捕获怪兽区','设施区',
        '手牌','迂返区','打出区')
    def __init__(self,father):
        # ---notebook部分
        ce=self.book=Notebook(father)
        f =self.frame=[]
        pageName=['记录','玩家']
        for i in range(2):
            f.append(Frame(ce, bg='grey', relief='sunken'))
            ce.add(f[i],text=pageName[i])
        self.message=ScrolledText(f[0],undo=True,fg='lightgreen',cursor='pencil',
            font='黑体 13',bg='grey')#,state='disabled
        ce.place(relwidth=1,relheight=0.9)
        self.message.place(relheight=1,relwidth=1)
        
        #height=2,
        # sf=self.showFrame=Frame(f[1],bg='paleturquoise')
        # # self.showFrame.place(rely=0.55,relheight=0.5,relwidth=1)
        sn=self.showNum=[IntVar(value=-1) for i in range(3)]
        self.var=IntVar(value=-1)
        self.button=[PlayerButton(f[1],'','黑体 15 bold',variable=self.var,value=i,
            indicatoron=0,anchor='nw',command=self.changePlayer) for i in range(8)]

        self.showVar=StringVar(value='一般怪兽区')
        sb=self.showButton=OptionMenu(f[1],self.showVar,command=self.show,*Other.place)
        nl=self.numLabel=Label(f[1],textvariable=sn[0],bg='lightgrey')
        # sb.bind('<<ComboboxSelected>>',self.show)
        # sb['value']=Other.place
        sb.place(rely=0.92,relwidth=0.8,relheight=0.08)
        nl.place(relx=0.8,rely=0.92,relwidth=0.2,relheight=0.08)

        self.throw=Button(father,text='弃牌堆',bg='grey',anchor='w',command=self.showThrow)
        self.deck =Button(father,text='卡组'  ,bg='grey',anchor='w',command=self.showDeck)
        self.throw.place(rely=0.9,relwidth=0.4,relheight=0.1)
        self.deck .place(relx=0.5,rely=0.9,relwidth=0.4,relheight=0.1)
        Label(father,textvariable=sn[1],bg='grey').place(relx=0.4,rely=0.9,relwidth=0.1,relheight=0.1)
        Label(father,textvariable=sn[2],bg='grey').place(relx=0.9,rely=0.9,relwidth=0.1,relheight=0.1)

    def show(self,event,show=True):
        '''展示一位玩家的某一区域'''
        who=self.var.get()
        name=self.showVar.get()
        place=Other.place.index(name)
        p=Player.player[who]
        if place==3:#手牌需要去掉空位
            card=[i for i in p.hand if i != None]
        else:
            card=p.guide[place]
        n=len(card)
        self.showNum[0].set(n)
        if show:
            Gui.askOne2(card,p.name,Other.place[place])

    def newMessage(self,text):
        '''消息框添加文本'''
        self.message.insert(END,text)
        self.message.see(END)
        
    def showThrow(self):
        '''展示玩家的弃牌堆'''
        who=self.var.get()
        p=Player.player[who]
        card=p.throw
        # Gui.isSpecial.set(false)
        Gui.askOne2(card,p.name,'弃牌堆')
        
    def showDeck(self):
        '''展示玩家的卡组'''
        i = self.var.get()
        return Player.player[i].showDeck()

    def newPlayer(self,name,without,first):
        '''游戏开始时,创建玩家的信息框'''
        for i in self.button:i.place_forget()
        self.total=len(without)
        self.first=first
        b=self.button
        p=Player.player
        for i in range(self.total):
            t=''
            if i<first:t+=str(self.total-first+i+1)
            else:t+=str(i-first+1)
            t+=':'+name[i]+'\n'
            for j in range(3):
                if without[i]!=j:t+=Card.char[j]
            Gui.newMessage(t)
            b[i].setText(t)
            b[i].changeImageWithPhoto(p[i].image)
            b[i].place(0.14*i)
        # b[i].pack(fill=X,pady=2)
        # father=self.frame[1]
        # t=self.tree=Treeview(father,columns=('1'))
        # t.heading('#0',text='name')
        # t.heading('#1',text='resource')
        # t.place(relheight=1,relwidth=1)
        # for i in range(self.total):
        # 	v=''
        # 	t.insert('',index=END,text=name[i],values=v)
        return

    def changePlayer(self):
        '''更改显示详细信息的玩家'''
        who=self.var.get()
        name=self.showVar.get()
        place=Other.place.index(name)
        p=Player.player[who]
        n=len(p.guide[place])
        self.showNum[0].set(n)
        n=len(p.throw)
        self.showNum[1].set(n)
        n=len(p.deck)
        self.showNum[2].set(n)
    
    def next(self):
        '''更新下一位玩家'''
        self.var.set(Player.now)
        self.changePlayer()

    def showShuffle(self,n):
        '''更新弃牌堆与卡组的数量'''
        self.showNum[1].set(0)
        self.showNum[2].set(n)

class Resource():
    """资源框的表头以及现有/备用资源数量展示"""
    def __init__(self,father):
        name=['信仰','钱币','食物']
        # self.label=[Label(father,font=['黑体',25],fg='lightgreen',
        # 	bg='darkcyan',text=name[x]) for x in range(9)]
        self.var=[IntVar() for i in range(6)]
        a=self.label=[Label(father,font=['黑体',14,'bold'],fg='lightgreen',
            bg='darkcyan',text=name[x]) for x in range(3)]
        b=self.resource=[Label(father,font=['黑体',16,'bold'],fg='lightgreen',
            bg='darkcyan',textvariable=self.var[x]) for x in range(3)]
        c=self.exResource=[Label(father,font=['黑体',16,'bold'],fg='lightgreen',
            bg='darkcyan',textvariable=self.var[x+3]) for x in range(3)]
        for i in range(3):
            a[i].place(relx=0.34*i,relheight=0.32,relwidth=0.32)
            b[i].place(relx=0.34*i,rely=0.335,relheight=0.32,relwidth=0.32)
            c[i].place(relx=0.34*i,rely=0.67,relheight=0.32,relwidth=0.32)
    
    def show(self,res):#
        for i in range(3):
            self.var[i].set(res[i])
    
    def showex(self):
        res=Player.exResource
        for i in range(3):
            self.var[i+3].set(res[i])

class Center(Basic):
    """中央牌堆的显示控制"""
    #button,text,var,people,card,cover
    placeName=['守矢神社','命莲寺','神灵庙','博丽神社','永远亭'
        ,'白玉楼','魔法之森','地灵殿','红魔馆','兽道','人间之里']
    theEmpty=[10]
    
    def __init__(self, father,*exceptOne):
        self.button: list[Radiobutton] = []
        c=self.button
        self.var=IntVar(value=-1)
        self.coverImage=findCardImage('cover')#背面图片
        self.remainCard=[0]*9
        
        height0=-0.038 #0.1
        weight0=0.178
        for i in range(9): #a is text,c is image
            # b.append(StringVar())
            # a.append(Radiobutton(father,textvariable=b[i],font=['黑体',13],
            # 	indicatoron=0,variable=self.var,value=i,command=self.toGain))
            c.append(Radiobutton(father, #bg='grey, #justify='center',
                indicatoron=0,variable=self.var,value=i,command=self.toGain))
            if(i!=8):
                # a[i].place(relx=(i%4)*0.2,rely=0.02 if i<4 else 0.5
                # 	,relheight=height0,relwidth=0.19,)#relwidth=0.19,
                c[i].place(relx=(i%4)*0.2,rely=(0.05 if i<4 else (0.52-height0) )+height0,
                    relwidth=weight0,relheight=0.42-height0)#width=160,height=160)#
        c[8].place(relx=0.8,rely=0.05+height0,relheight=0.42-height0,relwidth=weight0)#width=160,height=160,)
        for i in range(3):
            c.append(Radiobutton(father,command=self.toGain,#justify='center',
                indicatoron=0,variable=self.var,value=9+i))
            c[i+9].place(relx=0.8,rely=0.52+0.16*i,relwidth=weight0,relheight=0.16)		
            changeImageWithPhoto(c[i+9],findCardImage(f"10{i+6}"))
        # a[8].place(relx=0.8,rely=0.02,relheight=height0,relwidth=0.19)
        # for i in self.label:
        #i.bind('<Enter>',self.explain)
        Basic.__init__(self)

    def isOver(self,n)->bool:
        '''The game is over or not.At least number of players +1 of center is empty.'''
        return self.remain<=7-n

    def newGame(self):
        '''初始化中央牌堆的相关数据'''
        self.remain = 8
        Center.theEmpty = [10]
        exceptOne=randint(0,8)
        Gui.newMessage('被删除的牌堆为',Center.placeName[exceptOne])
        self.initCard(exceptOne)

        # Hand.pop(exceptOne)
        color=['green','orchid','palegoldenrod','crimson','paleturquoise',
        'pink','lightgrey','silver','orangered','lightgreen','burlywood']#
        color.pop(exceptOne)
        for i in range(9):
            # self.label[i].config(bg=color[i])
            self.button[i].config(bg=color[i])
            self.remainCard[i]=len(self.card[i])
    
    def initCard(self,exceptOne):	
        '''从Card类处重新填充中央牌堆'''		
        self.cover :list[Card]=[]
        self.card: list[Card] = [[] for s in range(13)]
        Card.newCenter(self.card,exceptOne)
        for i in range(12):#所有框设置图片,
            card=self.card[i].pop()
            self.cover.append(card)
            # if i<9:self.text[i].set(card.inCenter())
            if i < 9:
                changeImageWithCard(self.button[i], card)
            
    def explain(self,event):
        var=event.widget['value']
        c=self.cover[var]
        if(c==None):return #Gui.explain('已拿空')
        else:
            t=str(c)
            if(var<9):t+=f'\n\t\t\t\t\t\t(还剩余{self.remainCard[var]+1}张)'
            Gui.explain(t)

    def next(self,no):
        '''拿掉某一牌堆顶,翻开下一张'''
        if(no>8):return
        a=self.cover
        c=self.card[no]
        self.remainCard[no]-=1
        if(c==[]):#拿走最后一张,兽道不影响结束与否
            where=a[no].place
            if(no!=8):
                self.remain-=1
                Center.theEmpty.append(where)
            # self.text[no].set(Card.placeName[where])
            Gui.newMessage(f'{Center.placeName[where]}已拿空！')
            a[no]=None
            changeImageWithPhoto(self.button[no],self.coverImage)
            self.button[no]['state']='disable'
        else:
            changeImageWithPhoto(self.button[no],self.coverImage)
            self.button[no].update()
            sleep(0.2)
            a[no]=c.pop()
            # self.text[no].set(a[no].inCenter())
            changeImageWithCard(self.button[no],a[no])
            self.button[no].update()
            if a[no].hasMiracle():
                Player.checkMiracle(a[no].name)

    @whenClickOn
    def toGain(self):
        '''玩家想要获得某一中央卡牌。'''
        v=self.var.get()
        c=self.cover[v]
        if(c==None):return #已经拿空了，无响应
        self.var.set(-1)
        Player.cp.gain(v)
    
    def checkMiracle(self):
        '''检查是否触发奇迹'''
        for i in range(8):
            if self.cover[i].hasMiracle():
                Player.checkMiracle(self.cover[i].name)

    def askEmpty(self) ->set:
        '''打印已拿空牌堆并返回相应地点代码'''
        name=''
        for i in Center.theEmpty:
            name+=Center.placeName[i]+' '
        Gui.newMessage('已拿空:',name)
        res=set(Center.theEmpty)
        return res

    def sortThree(self,no):
        '''幽幽子的折扇的特殊函数，给某一牌堆顶的三张排序'''
        '''return fun(*arg) if Gui.ds.isEmpty() else Gui.ds.get()'''
        
        # 准备被排序对象
        card=[]
        all=self.card[no]
        if len(all)>1:
            card.append(all.pop())
            card.append(all.pop())
        else:
            card=all
        cover=self.cover[no]
        card.append(cover)
        
        # 修改并放回
        card=Gui.sort(card,'幽幽子的折扇')
        newCover=card.pop()
        self.cover[no]=newCover
        # self.text[no].set(newCover.inCenter())
        changeImageWithCard(self.button[no],newCover)
        self.button[no].update()
        if  newCover.hasMiracle(): #是否触发还存疑
            Player.checkMiracle(newCover.name)
        all+=card

class Hand(Basic):
    '''手牌的显示控制'''
    color=['green','orchid','yellow','red','paleturquoise',
        'pink','lightgrey','silver','orangered','lightgreen','burlywood']
    # placeName=['守矢神社','命莲寺','神灵庙','博丽神社','永远亭'
    # 	,'白玉楼','魔法之森','地灵殿','红魔馆','兽道','人间之里']
    
    def __init__(self,father):
        self.num,self.max=0,0
        self.weight=0.14
        # t=self.text=[None]*35
        #self.index=[]#self.max=0
        #代表showing的数量
        self.var=IntVar(value=-1)
        self.button:list[CardButton]=[None]*50
        a = self.button
        self.card:list[Card]=[]
        self.showing=[]
        for i in range(50):
            #self.index.append(i+1)
            # t[i]=StringVar()#justify='center',#command=self.toGain
            a[i]=CardButton(father,#['黑体',16],
                bg='darkcyan',indicatoron=0,variable=self.var,
                value=i,compound='bottom',command=self.use)
            a[i].bind(self.explain)
    
    @whenClickOn
    def use(self):
        '''玩家点击手牌的回调函数'''
        # if(Gui.isSpecial):return
        # print('Call back for using',flush=True)
        index=self.var.get()
        self.var.set(-1)
        Player.cp.use(index)
    
    def showText(self,i):
        '''返回文本的同时会更换图片'''
        c=self.card[i]
        #changeImageWithCard(self.button[i],c)#
        if c!= None:self.button[i].changeImageWithCard(c)
        if c==None:
            Gui.newMessage(f'第{i}张牌出错')
            return None
        return c.inHand()
    
    def show(self,card:list[Card]):
        '''新玩家刷新手牌'''
        # 注意不要用列表做默认常数，不然是持续存在且可变的
        self.num=self.max=len(card)
        self.card=card
        self.place_forget()
        for i in range(self.num):
            self.button[i].changeImageWithCard(self.card[i])
        self.showing=self.button[:self.num]
        self.rePlace()
        # t=self.showText(i)
        # if t!=None:self.text[i].set(t)
        # else:self.showing.pop(i)

    def append(self):
        '''添加一张手牌，包括设置文本图片，以及放置.
        流程：根据值找到新框并设置，然后加入showing		'''
        b=self.button[self.max]
        card=self.card[-1]
        # if card==None:print(card)
        # else:self.text[m].set(card.inHand())
        b.changeImageWithCard(card)
        self.showing.append(b)
        self.max+=1
        self.num+=1
        # 6张手牌是全放置的上限,刚好为7张时需要重新放置
        if(self.num==7):self.rePlace()
        else:	 		self.place()
    
    def lost(self,no):
        '''先根据value来找到并隐藏,然后安置后面的卡牌'''
        s=self.showing
        i=0
        # 先根据value来找到并隐藏
        while i <self.num:
            if(s[i].var==no):
                self.num -= 1
                s[i].place_forget()
                s.pop(i)
                break
            i+=1
        #再安置后面的卡牌
        n=self.num
        if  (n>6):#只要手牌多就必须重放
            self.rePlace()
        elif(n!=i):self.rePlace(i)
        #else#手牌少且刚好最后一张，无事发生
    
    def rePlace(self,first=0):
        '''这种放置方式下，所有牌的位置都要变化'''
        # fix=0
        n=self.num
        if(n<8):x=self.weight
        else:   x=1/n
        for i in range(first,n):#
            self.showing[i].placeHand(x*i)
            # if self.card[i]!=None:
            # else:fix-=x
            #relx=,relwidth=0.15,relheight=1
    
    def place(self):
        '''单纯添加一张手牌时,根据最终数量的多少来放置'''
        n=self.num
        if(n<8):#手牌少时,只把新牌添加到末尾
            n-=1
            self.showing[n].placeHand(self.weight*n)
            #relx=0.15*n,relwidth=0.15,relheight=1
        else: #手牌多时，需要从头到尾重放
            x=1/n
            for i in range(1,n):
                self.showing[i].placeHand(x*i)
                #relx=x*i,relwidth=0.15,relheight=1
    
    def place_forget(self,*event):
        '''隐藏所有控件'''
        for i in self.showing: i.place_forget()

class Top():
    '''多张选定卡牌的显示与选择框'''
    
    def __init__(self,father):
        a=self.top=Toplevel(father,bg='grey')
        a.protocol('WM_DELETE_WINDOW',self.canNotDelete)
        w = father.winfo_screenwidth()
        h = father.winfo_screenheight()
        a.geometry("%dx%d+%d+%d" %(1000,300,280,200))#w*0.8,h/2.5,w/5,h/4
        a.withdraw()
        self.tip=StringVar()
        self.tipLabel=Label(a,font=['黑体',15],bg='lightgrey',
            textvariable=self.tip)
        self.tipLabel.place(relx=0.1,relheight=0.1,relwidth=0.8)
        self.var=IntVar(value=-1)
        ce=self.center=Notebook(a)
        f=self.frame=[]
        for i in range(8):
            f.append(Frame(ce,bg='grey'))
            ce.add(f[i],text=f'第{i+1}页')
        ce.place(rely=0.1,relwidth=1,relheight=0.75)
        t=self.text=[] #[None]*25
        self.button:list[CardButton]=[]
        #self.frame=Frame(a,bg='grey')
        for i in range(48):
            t.append(StringVar(value=i))
            self.button.append(CardButton(f[i//6],#['黑体',12],
                indicatoron=0,value=i,bg='paleturquoise',variable=self.var))
            self.button[i].bind(self.explain)
        self.card=[]
        self.cancel=IntVar(value=-1)
        # self.confirmButton=Radiobutton(a,text='confirm',value=1,variable=self.cancel,indicatoron=0)
        # self.confirmButton.place(relx=0.35,rely=0.9,relwidth=0.15,relheight=0.1)
        self.cancelButton =Radiobutton(a,text='取消', value=-2,variable=self.var,indicatoron=0)
        self.cancelButton .place(relx=0.4, rely=0.85,relwidth=0.15,relheight=0.15)

    def explain(self,event):
        index=event.widget['value']
        c=self.card
        if(index>=len(c)):return
        Gui.explain(c[index])
        
    def canNotDelete(self):
        '''提示禁止退出窗口'''
        oldText=self.tip.get()
        self.tip.set('Please do not delete!')
        self.top.update()
        sleep(1.5)
        self.tip.set(oldText)
        
    def place(self,n):
        '''卡牌框放置'''
        for i in range(n):
            #self.button[i].pack(side='left')
            self.button[i].place(i%6*0.16,0)
    
    def show(self,page=1):
        '''应该根据显示内容更改展示页数?目前没用上...'''
        for i in range(page*6+6):
            #self.button[i].pack(side='left')
            self.button[i].place(i%6*0.15,0)
        
    def beReady(self):
        """ 选择操作前的一般流程：显示窗口，选中第一页，设置等待变量为-1 """
        self.top.deiconify()
        self.center.select(0)
        self.var.set(-1)
        
    def place_forget(self,n):
        '''隐藏卡牌框'''
        for i in range(n):
            self.button[i].place_forget()
    
    def askOneToExile(self,card,inThrow,no,
        title='',tip='选一张放逐:'):
        '''单纯适用于放逐弃牌堆和手牌中的一张牌'''
        self.top.title(title)
        n=len(no)
        tip+=f'。共{n}张,其中前{inThrow}张来自弃牌堆'
        self.tip.set(tip)
        self.card=card
        #self.top.geometry("%dx%d+%d+%d" %(300,n*70,600,400))
        for i in range(n):
            self.button[i].changeImageWithCard(card[i])
        self.place(n)
        self.beReady()
        while(True):
            sleep(0.05)
            self.top.update()
            ask=self.var.get()
            if(ask!=-1):
                self.top.withdraw()
                self.place_forget(n)
                # if(ask==-2):
                # 	print('cancel!')
                # print('choose %d' %(ask))
                return ask

    def askOne2(self,card,title='',tip='选择一张:'):
        '''单纯地从特定卡牌中选择一张，不用于放逐'''
        self.top.title(title)
        n=len(card)
        if n>48:n=48
        if tip!='':tip+='.'
        tip+=f'共{n}张'
        self.tip.set(tip)
        self.card=card
        #self.top.geometry("%dx%d+%d+%d" %(300,n*70,600,400))
        for i in range(n):
            # self.text[i].set(card[i].inHand())
            self.button[i].changeImageWithCard(card[i])
        self.place(n)
        self.beReady()
        while(True):
            sleep(0.05)
            self.top.update()
            ask=self.var.get()
            if(ask!=-1):
                self.top.withdraw()
                self.place_forget(n)
                # if(ask==-2):
                # 	print('Cancel!')
                return ask

    def sort(self,card,title='',tip='请排序，先选择的在下:')->list[Card]:
        '''对选择的牌排序,返回一个排序后的列表'''

        n = len(card)
        if ds.hasVal():  # 能取值，就直接获取
            temp=card[:]
            for i in range(n):
                card[i]=temp[ds.get()]
            return card
        
        # 事前准备
        oldState=Gui.isSpecial
        Gui.isSpecial=True
        self.top.title(title)
        self.tip.set(tip)
        self.card=card
        for i in range(n):
            # self.text[i].set(str(i+1)+':'+card[i].inHand())
            self.button[i].changeImageWithCard(card[i])
        self.place(n)
        self.beReady()

        # 逐个询问
        order=[]
        while(True):
            sleep(0.05)
            self.top.update()
            ask=self.var.get()
            if( ask>-1 ):
                ds.add(ask)
                order.append(card[ask])
                self.button[ask].place_forget()
                n-=1
                if n==0:
                    self.top.withdraw()
                    Gui.isSpecial=oldState
                    break
                self.var.set(-1)
        return order
         
class Fbutton(Basic):
    '''设施相关控件'''
    
    def __init__(self,father):
        a=self.button=[]
        b=self.text=[]
        self.var=IntVar(value=-1)
        self.state,self.over=[],[]
        for i in range(9):
            b.append(StringVar())
            a.append(Radiobutton(father,bg='grey',indicatoron=0,
                font=['黑体',12],fg='lightgreen',
                textvariable=b[i],variable=self.var,value=i,command=self.launch))
            a[i].place(rely=i*0.125,relwidth=0.98,relheight=0.125)
        Basic.__init__(self)

    @whenClickOn
    def launch(self):
        '''发动选中的设施'''
        # if(Gui.isSpecial):return
        index=self.var.get()
        self.var.set(-1)
        Player.cp.launch(index)

    def show(self,cards):
        self.card=cards
        self.over.clear()
        n=len(cards)
        if(n>8):n=8
        for i in range(n):
            self.ableOne(i)
        for i in range(n,8):
            self.disbaleOne(i)

    def showText(self,i):
        '''同时设置控件的颜色，表示是否能发动'''
        if self.card[i].canBeClick():
            self.button[i].config(bg='darkcyan')
        else:
            self.button[i].config(bg='grey')
        self.button[i]['state']='normal'
        return self.card[i].name
    
    def lost(self,no):
        '''失去一个建筑'''
        if(no >7):
            return
        l = len(self.card)
        b=self.button
        for i in range(no,min(8,l)):
            self.text[i].set(self.card[i].name)
            nextbg=b[i+1]['bg']
            b[i].config(bg=nextbg)
        if l<8:
            self.disbaleOne(l)

    def record(self):
        '''记录已发动的情况'''
        self.state=[]
        for i in self.button:
            if i['bg']!='darkcyan':self.state.append(False)
            else:self.state.append(True)
    
    def reset(self,card):
        '''根据记录,还原设施区'''
        self.card=card
        n=len(card)
        if(n>8):n=8
        for i in range(n):
            if self.state[i]:self.button[i].config(bg='darkcyan')
            else:self.button[i].config(bg='grey')
            self.text[i].set(card[i].name)
        for i in range(n,9):
            self.text[i].set('')
            self.button[i].config(bg='grey')

    def setLaunched(self,no):
        '''给已发动的设施标注状态'''
        if no>7:return
        b=self.button[no]
        b['bg']='grey'
    
class Mbutton(Basic):
    '''妖怪区域的控件'''

    def __init__(self,father):
        a=self.button=[]
        b=self.text=[]
        self.var=IntVar(value=-1)
        for i in range(9):
            b.append(StringVar())
            a.append(Radiobutton(father,bg='grey',indicatoron=0,
                font=['黑体',12],fg='lightgreen',
                textvariable=b[i],variable=self.var,value=i,command=self.catch))
            a[i].place(rely=i*0.125,relwidth=0.98,relheight=0.125)
        Basic.__init__(self)

    @whenClickOn
    def catch(self):
        '''捕获的回调函数'''
        # if(Gui.isSpecial):return
        index=self.var.get()
        self.var.set(-1)
        Player.cp.catch(index)
        
    def lost(self,no):
        '''删除一项,然后刷新'''
        l=len(self.card)
        for i in range(no,min(l,8)):
            self.text[i].set(self.showText(i))
        if l<8:
            self.disbaleOne(l)

    def disbaleOne(self, i):
        '''将控件设为不可用'''
        self.text[i].set('')
        self.button[i]['state'] = 'disable'

class Tip():
    '''界面上的buff和操作提示框'''

    def __init__(self,father,isCancel):
        self.var=isCancel#IntVar(value=0)
        f=self.frame=[ Frame(father) for i in range(2)]
        f[0].place(relx=0.1,relwidth=0.9,relheight=0.5)
        f[1].place(relx=0.1,rely=0.5,relwidth=0.9,relheight=0.5)
        names=['赛钱箱1','神子','洋馆','白莲','紫苑',
        #		  0	   1	  2	 3	  4 
        '女苑','御柱','阿哞','神奈子',
        # 5	   6	 7	 8
        '纳兹琳','赛钱箱2','芳香','蕾米','','走廊']
        #9		10		 11   12   13   14
        self.label=[Label(f[0],bg='paleturquoise',text=names[i]
            ) for i in range(15)]
        self.showing=[]
        self.image=Label(father,bg='grey')
        self.image.place(relheight=1,relwidth=0.1)
        self.button=Button(f[1],text='结束',bg='grey',command=self.end)
        self.button.place(relx=0.9,relheight=1,relwidth=0.1)
        self.cancel=Button(f[1],text='取消',bg='grey',command=self.cancel)
        self.cancel.place(relx=0.8,relheight=1,relwidth=0.1)
        self.text=StringVar()
        self.tip=Label(f[1],textvariable=self.text,bg='lightgrey',font=['黑体',12])
        self.tip.place(relheight=1,relwidth=0.8)

    @whenClickOn
    def end(self):
        '''结束回合的回调函数'''
        Player.endAndNext()
    
    def setTip(self,text):
        '''设置提示文本'''
        self.text.set(text)
        self.tip.update()

    # @whenClickOn
    def cancel(self):
        '''设置为取消的状态'''
        self.var.set(True)

    def append(self,i):
        '''添加一个新buff'''
        self.pack(i)
        if i==0:
            self.pack(10)
            
    def lost(self,i):
        '''失去buff'''
        self.label[i].pack_forget()
        self.showing.remove(i)
    
    def flash(self,image,show=True):
        '''新玩家刷新控件,必然刷新头像，（可选）刷新其他控件'''
        if show:
            for i in self.showing:
                self.label[i].pack_forget()
            self.showing=[]
            for n, i in enumerate(Player.buff):
                if i:
                    self.pack(n)
        changeImageWithPhoto(self.image,image)

    def pack(self,i):
        '''在末尾添加新buff文字框'''
        self.label[i].pack(side='left',padx=2)
        self.showing.append(i)

class SmallTop():
    '''小型的询问数字,种类的窗口'''

    char=['★','◎','♨']
    def __init__(self,father):
        a=self.top=Toplevel(father,bg='grey')
        a.protocol('WM_DELETE_WINDOW',self.canNotDelete)
        #a.geometry("%dx%d+%d+%d" %(60,100,w/2.5,h/2.5))
        a.withdraw()
        self.tip=StringVar()
        self.tipLabel = Label( 
            a, bg='lightgrey', font=['黑体', 18], textvariable=self.tip, wraplength=300)
        self.tipLabel.pack()
        t=self.text=[]
        b=self.button=[]
        self.var=IntVar(value=-1)
        self.cancel=Radiobutton(a,text='取消',
            variable=self.var,value=-2,indicatoron=0,)
        for i in range(10):
            t.append(StringVar()) #justify='center',#command=self.toGain
            b.append(Radiobutton(a,textvariable=t[i],font=['黑体',16],
                bg='lightgrey',indicatoron=0,variable=self.var,
                value=i,compound='bottom')) 
    
    def pack_forget(self,n):
        '''隐藏选项控件以及取消按钮'''
        for i in range(n):self.button[i].pack_forget()
        self.cancel.pack_forget()
        
    def askANumber(self,n=2,title='',tip=''):
        '''用于询问一个数字'''
        self.top.title(title)
        self.tip.set(tip)
        if n>6:n=6
        n += 1
        self.top.geometry("%dx%d+%d+%d" % (300, n*70, 600, 400))
        for i in range(n):
            self.text[i].set(i)
            self.button[i].pack(fill=X,padx=2)
        self.cancel.pack()
        self.top.deiconify()
        self.var.set(-1)
        while(True):
            sleep(0.2)
            self.top.update()
            ask=self.var.get()
            if(ask!=-1):
                self.pack_forget(n)
                self.top.withdraw()
                return ask
                
    def askAType(self,types=[0,1,2],title='',tip='选择要消耗的资源:'):
        '''用于询问资源种类'''
        self.tip.set(tip)
        self.top.title(title)
        n=len(types)
        self.top.geometry("%dx%d+%d+%d" %(300,n*70,600,400))
        for i in types:
            self.text[i].set(SmallTop.char[i])
            self.button[i].pack(fill=X,padx=2)
        self.cancel.pack()
        self.top.deiconify()
        self.var.set(-1)
        while(True):
            sleep(0.2)
            self.top.update()
            ask=self.var.get()
            if(ask!=-1):
                self.pack_forget(3)
                self.top.withdraw()
                return ask
                
    def canNotDelete(self):
        oldText=self.tip.get()
        self.tip.set('Please do not delete!')
        self.top.update()
        sleep(0.5)
        self.tip.set(oldText)

class HomePage():
    '''进入游戏的开始界面,与玩家的设置界面，联网时改为'''
    # title一直没有单独隐藏,而是随着整体隐藏,倒也无伤大雅
    #canvas,home,title,button,choose

    def __init__(self, r):
        """ 初始化界面 """
        # 背景板以及标题栏
        self.canvas = Label(r, bg='#D2B48C')
        """ 在TK窗口下的一个全覆盖框体,canvas """
        changeImageWithName(self.canvas, 'homepage')
        self.title = Label(self.canvas, text='微型\n幻想乡', font='粗体 40 bold')
        self.title.place(relx=0.4, rely=0.1, relheight=0.2, relwidth=0.2)

        # 放置三个按钮
        root = self.home = Label(self.canvas, bg='palegoldenrod')
        """ 用来放置三个按钮的框体 """
        self.button: list[Button] = []
        text = ['网络连接', '------', '退出']
        fun = [self.newGame, self.quickGame, r.quit]  # self.loadGame,
        for i in range(3):
            self.button.append(Button(
                root, font='粗体 14 bold', text=text[i], command=fun[i]))
            self.button[i].place(rely=i*0.337, relwidth=1, relheight=0.325)

        # 房间页面对象
        f = Frame(self.canvas, bg='grey')
        self.choose = RoomPage(
            f, self, lambda: Gui.gaimingPage.place(relheight=1, relwidth=1))

    def newGame(self):
        '''新游戏询问人数，然后进入设置界面'''
        self.home.place_forget()
        self.choose.place()

    def place(self):
        '''放置背景以及快捷按钮'''
        self.canvas.place(rely=0,relheight=1, relwidth=1)
        self.home.place(relx=0.4, rely=0.5, relwidth=0.2, relheight=0.3)

    def place_forget(self):
        '''进入游戏时,整体隐藏'''
        self.canvas.place_forget()

    def quickGame(self):
        pass

    def startGame(self):
        name, photo, res=[],[],[]
        self.place_forget()
        for i,j,k in Info.getPlayerInfo():
            name.append(i)
            photo.append( findHeadImage(j) )
            res.append( k )
        Gui.gaming(name, photo, res)
    


class Gui():
    """控制展示所有界面控件"""
    root =Tk()
    Card.createImage()
    Card.readData()
    haveInit=False
    isSpecial=False
    placeText=['中央牌堆','设施区','手牌']
    #frameList=[Frame(cls.root) for i in range(6)]
    resource:Resource=None
    other:Other=None
    monster:Mbutton =None
    facility:Fbutton=None
    center  :Center=None
    tip:Tip=None
    hand:Hand=None
    smallTop:SmallTop=None
    top:Top=None
    homepage:HomePage=None

    def canNotDelete():
        if messagebox.askyesno('关闭游戏？','是否要关闭游戏？'):
            Gui.root.quit()
    
    def init():
        if (Gui.haveInit):return
        r1=Gui.root
        r1.protocol('WM_DELETE_WINDOW',Gui.canNotDelete)
        # r1.attributes("-alpha", 0.9)
        r1.title('微型幻想乡')#Micro Gensokyo
        w,h=1280,700
        #w = r.winfo_screenwidth()
        #h = r.winfo_screenheight()-100
        r1.geometry("%dx%d+0+0" %(w,h))
        r1.attributes("-topmost",False)
        r=Gui.gaimingPage=Frame(Gui.root,bg='grey')
        Gui.root.attributes("-alpha", 90/100)

        # r.place(relheight=1,relwidth=1)
        Gui.frameList:list[Frame]=[Frame(r,bg='grey') for i in range(8)]
        #	  文本,资源,妖怪,设施, 中央， 其他，提示，手牌
        x=	 [0  ,0   ,0   ,0.1 ,0.2  ,0.8  ,0.2  ,0.2]
        y=	 [0  ,0.4 ,0.55,0.55,0	,0	,0.625,0.725]
        height=[0.4,0.15,0.45,0.45,0.625,0.725,0.1  ,0.275]
        width =[0.2,0.2 ,0.1 ,0.1 ,0.6  ,0.2  ,0.6  ,0.8]
        
        f=Gui.frameList
        background=['grey','grey','grey','grey',"grey",
            'lightgrey',"grey","grey"]
        for i,a in enumerate(f):
            a['bg']=background[i]
            a.place(relx=x[i],rely=y[i],
                relwidth=width[i],relheight=height[i])

        Gui.explaintion=StringVar()
        Gui.isCancel=BooleanVar()
        Message(Gui.frameList[0],textvariable=Gui.explaintion,relief='sunken',
            bg='grey',anchor='nw',justify='left',fg='lawngreen',font=['黑体',12]
            ).place(relwidth=1,relheight=1)#wraplength='400', 
        Gui.resource:Resource=Resource(f[1])
        Gui.other:Other=Other(f[5])
        Gui.monster:Mbutton =Mbutton(f[2])
        Gui.facility:Fbutton=Fbutton(f[3])
        Gui.center  :Center=Center(f[4])
        Gui.tip:Tip=Tip(f[6],Gui.isCancel)
        Gui.hand:Hand=Hand(f[7])
        Gui.smallTop:SmallTop=SmallTop(r)
        Gui.top:Top=Top(r)
        Gui.homepage:HomePage=HomePage(Gui.root)
        #0 cen,1 fac,2 hand
        Gui.var=[Gui.center.var,Gui.facility.var,
            Gui.hand.var]#Gui.monster.var,
        Gui.haveInit=True
        Player.bind()
        #Gui.avatar=Avatar(Gui.frameList[3])
        #Gui.root.bind('<KeyPress-1>',Player.useAll)

    def gaming(name=None,photo=None,res=None):
        Gui.center.newGame()
        Gui.gaimingPage.place(relheight=1,relwidth=1)
        Player.init(name,photo,res)

    def returnHome(event):
        if messagebox.askyesno('!','是否返回主界面'):
            # Gui.center.remain=8
            # Player.clear()
            Gui.gaimingPage.place_forget()
            Gui.homepage.place()

    def showHome():
        Gui.homepage.place()
    
    def nextCenter(no):
        Gui.center.next(no)
        
    def getCover(no):
        return Gui.center.cover[no]		
    				
    def setTip(text=''):
        """ 设置提示，不撤销 """
        Gui.tip.setTip(text)
    
    def explain(text):
        Gui.explaintion.set(text)
    
    def showResource(res):
        Gui.resource.show(res)

    def showexResource():
        Gui.resource.showex()

    def flash(p,reset=True):
        '''更新新玩家的界面 ，reset代表是否会重置设施区'''
        Gui.monster.show(p.monster)
        if reset:
            Gui.facility.show(p.facility)
            Gui.other.next()
        else:
            Gui.facility.reset(p.facility)
            # Gui.tip.flash(p.image,False)
        p.neatHand()
        Gui.hand.show(p.hand)
        Gui.tip.flash(p.image)

    def handAppend():
        Gui.hand.append()
    
    def handLost(n):
        Gui.hand.lost(n)
    
    def facilityAppend():
        Gui.facility.append()
    
    def facilityLost(n):
        Gui.facility.lost(n)
    
    def facilityLaunch(no):
        Gui.facility.setLaunched(no)
        
    def monsterAppend():
        Gui.monster.append()
    
    def monsterLost(no):
        Gui.monster.lost(no)
    
    def isGameOver(n):
        return Gui.center.isOver(n)
    
    @whenClickOn
    def end(event):
        if not Player.haveInit:return 
        Player.endAndNext()

    @whenAsk
    def askVar(no,tip=None):
        '''询问中央牌堆、手牌、设施、妖怪之一的一个值'''
        # no:center facility hand
        # oldState=Gui.isSpecial
        Gui.isSpecial=True
        Gui.var[no].set(-1)
        ask=-1
        if tip==None:
            Gui.setTip(f'请选择{Gui.placeText[no]}一张牌：')
        else:
            Gui.setTip(tip)
        Gui.isCancel.set(False)
        while True:
            sleep(0.05)
            Gui.root.update()
            if Gui.isCancel.get():
                ask=-2
                break
            ask=Gui.var[no].get()
            if(ask!=-1):
                Gui.var[no].set(-1)
                break
        Gui.isSpecial=False
        Gui.setTip('')
        return ask

    @whenAsk
    def askAType(moreThan3=[0,1,2],title='',tip='选择资源种类'):
        '''如果不选择，则返回None'''
        Gui.isSpecial=True
        a=Gui.smallTop.askAType(moreThan3,title,tip)
        Gui.isSpecial=False
        return a if a>-1 else None

    @whenAsk
    def askANumber(*arg):
        Gui.isSpecial=True
        a=Gui.smallTop.askANumber(*arg)
        # a=Gui.smallTop.askANumber(moreThan3,title,tip)
        Gui.isSpecial=False
        return a

    @whenAsk
    def askOne(card,inThrow,no,title='',tip='选一张放逐'):
        '''用于放逐'''
        oldState=Gui.isSpecial
        Gui.isSpecial=True
        r=Gui.top.askOneToExile(card,inThrow,no,title,tip)
        Gui.isSpecial=oldState
        return r

    @whenAsk
    def askOne2(card, title='', tip=''):
        '''放逐以外的单选流程'''
        oldState=Gui.isSpecial
        Gui.isSpecial=True
        r=Gui.top.askOne2(card,title,tip)
        Gui.isSpecial=oldState
        return r
    
    @classmethod
    def newMessage(cls,*text):
        '''逐个打印'''
        t='\n'
        for i in text:
            t+=str(i)
        cls.other.newMessage(t)

    def sort(*args):
        return Gui.top.sort(*args)

    def checkMiracle():
        Gui.center.checkMiracle()

    def newPlayer(name,without):
        Gui.other.newPlayer(name,without)

    def askEmpty():return Gui.center.askEmpty()

    def record():
        Gui.facility.record()

    def showShuffle(n):
        '''更新卡组和弃牌堆的数量'''
        Gui.other.showShuffle(n)

    def changeColor(e):
        color=simpledialog.askstring(title='',prompt='')
        Gui.frameList[4]['bg']=color
    
    # def launchOne(no):
    #     Gui.facility.launchOne(no)

    def beNormal(event):
        Gui.isSpecial=False

    def changeAlpha(event):
        no=simpledialog.askinteger('','请输入透明度（百分比%）')
        Gui.root.attributes("-alpha", no/100)

    def setSeed(*e):
        s=simpledialog.askinteger('set seed','seed value')
        seed(s)
    
    def askRecur(*args):
        if messagebox.askyesno('', '是否要重现操作？'):
            Player.recurAll(simpledialog.askstring(
                title='File name:', prompt='Input the file name:'))

from .player import Player

if __name__ == "__main__":
    r1=Tk()
    # r1.protocol('WM_DELETE_WINDOW',canNotDelete)
    r1.attributes("-alpha", 0.95)
    r1.title('微型幻想乡')#Micro Gensokyo
    w,h=1280,800
    #w = r.winfo_screenwidth()
    #h = r.winfo_screenheight()-100
    r1.geometry("%dx%d+0+0" %(w,h))
    r1.attributes("-topmost",True)
    # r=Gui.gaimingPage=Frame(root,bg='grey')
    HomePage(r1).place()
    r1.mainloop()



    # def shuffleAndShow(cards):
    # 	name,num,no=[],[],0
    # 	for i in cards:
    # 		j=findIndex(name,i.name)
    # 		if  j!=None:
    # 			num[j]+=1
    # 		else:
    # 			name.append(i.name)
    # 			num.append(1)

    # 	text=''
    # 	for i in range(len(num)):
    # 		text+=f'{num[i]}x{name[i]}\n'
    # 	text=text[:-1]
    # 	Gui.newMessage(self.name,'的卡组:\n',text)
    
    # def launchAll(self,event):
    #     '''发动界面上的设施，目前没用上'''
    #     for n, i in enumerate(self.button):
    #         if i['bg']!='grey':
    #             self.var.set(n)
    #             self.launch()

    # def hadLaunch(self,no):
    #     b=self.button[no]
    #     b['bg']='grey'
