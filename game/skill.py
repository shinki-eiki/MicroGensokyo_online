
from dataTransfer.dataStorage import DataStorage as ds
import game.player as player
# from .player import player.Player
from .GUI import Gui
from .card import Card
from .dialog import simpledialog, messagebox
from .information import Info
from .con_fun import whenOperateion, afterOperation
from .netMessage import NetMessage
from .information import Info

# exile,放逐,res,resour的缩写,char,character的缩写
from time import sleep
from random import shuffle, randint


def gainResource(t, n=1):
    if(n == 0):
        return
    r = player.Player.resource
    r[t] += n
    Gui.resource.var[t].set(r[t])


def getFaith(n=1):
    gainResource(0, n)


def getMoney(n=1):
    gainResource(1, n)


def getRice(n=1):
    gainResource(2, n)


def resourceChange(a, b, lost=-3, gain=2):
    if(player.Player.resource[a] < -lost):
        Gui.newMessage('资源不足!')
        return 1
    gainResource(a, lost)
    gainResource(b, gain)


def appendBuff():
    player.Player.appendBuff(Skill.card.name)


def gainChangeabledRes(t=[0, 1, 2], n=1):
    theType = Gui.askAType(t, f'请选择想要获得的资源种类,数量为{n}')
    if(theType == -2):
        return 1
    gainResource(theType, n)


def lostHand():
    if player.Player.cp.handNumber() == 0:
        return 0
    while True:
        no = Gui.askVar(2, '可以弃一张牌,然后获得资源：')
        if(no == -2):
            return 0
        else:
            card = player.Player.cp.hand[no]
            if card.name != Skill.card.name:
                player.Player.cp.lost(no)
                break


def copyEffect(card, coper):
    Gui.newMessage(f'复制了{card.name}的效果')
    player.Player.cp.gainResourse(card)
    Skill.spell(card)


def copyChar(faith=False):
    card = []
    coper = Skill.card
    findUsedChar(card, faith)
    if(card == []):
        Gui.newMessage('没有卡可以复制!')
        return
    r = Gui.askOne2(card, Skill.card.name,
                    '选择一张复制其效果：')
    if(r == -2):
        return 1
    else:
        return copyEffect(card[r], coper)


def findUsedChar(card, faith):
    for i in player.Player.used:
        if(i.category() == 0):
            if(faith and not i.isFaith()):
                continue
            card.append(i)


def selfDestory():
    p = player.Player.cp
    name = Skill.card.name
    return p.selfDestory(name)


def gainCenter(cost=15, category=[0, 1, 2]):
    while True:
        t = '选择中央牌堆一张'
        typeList = ['角色', '设施', '妖怪']
        for i in category:
            t += typeList[i]+'/'
        t += f'（费用不高于{cost}）'
        no = Gui.askVar(0, t)
        if no == -2:
            return 1
        card = Gui.getCover(no)
        if card.category() in category and card.totalCost() <= cost:
            p = player.Player.cp
            p.obtain(card, no)
            return
        else:
            Gui.setTip('不满足条件！')
            sleep(2)


def tongNian():
    if(not player.Player.faithCard):
        return 0  # 通念


def qiaoShou():
    if(len(player.Player.cp.facility) < 2):
        return 0  # 巧手


def draw2(): player.Player.drawP(2)


def draw3(): player.Player.drawP(3)

def exileHand():
    p = player.Player.cp
    while True:
        no = Gui.askVar(2, '可以放逐一张手牌')
        if(no == -2):  # 不放逐
            # print('cancel.')
            return 0
        else:
            card = p.hand[no]
            if card.name != Skill.card.name:
                p.hand[no] = None
                Gui.handLost(no)
                player.Player.exileAdd(card)
                return


def justExileCenter(category=[0, 1, 2]):
    while True:
        Gui.setTip('可以放逐中央牌堆顶一张牌.')
        no = Gui.askVar(0)
        if no > 8:
            Gui.newMessage('除了人间之里！')
            continue
        elif(no == -2):
            return 0
        else:
            card = Gui.getCover(no)
            if(card != None and card.category() in category and card.name != '毛玉王'):
                Gui.nextCenter(no)
                player.Player.exileAdd(card)
                return


def exileCenter():
    while True:
        Gui.setTip('可以放逐中央牌堆顶一张牌.')
        no = Gui.askVar(0)
        if no > 8:
            Gui.setTip('除了人间之里！')
            sleep(2)
            continue
        elif (no == -2):
            return None
        else:
            card = Gui.getCover(no)
            if card.name != '毛玉王':
                player.Player.exileAdd(card)
                Gui.nextCenter(no)
                return card

# ---------------|basic function|-----------------------


class Skill():
    card = None
    """ 当前正在处理效果的卡牌 """
    no, cardTemp = [], []
    """ 业障化身专用的数组,记录 """
    end = []
    """ 记录结束阶段的效果,包括karma,sakuya """
    function = []

    def checkEnd():
        '''检查结束效果,包括业障以及咲夜'''
        if Skill.end == []:
            return
        if 0 in Skill.end:  # karma
            where = []
            total = len(Skill.no)
            p = player.Player.cp
            allCard = [p.throw, p.deck, p.hand,
                    p.facility, p.repeat, player.Player.exile]
            w = 0
            no, c = Skill.no, Skill.cardTemp
            pls = player.Player.player
            #
            for i in allCard:  # 找牌,删牌,i是牌堆位置
                o = 0
                for card in i:
                    if card == None:
                        continue
                    name = card.name
                    if name in c:
                        # print(o,':',name)
                        index = c.index(name)
                        who = no.pop(index)
                        c.pop(index)
                        pls[who].throw.append(card)
                        i[o] = None
                        Gui.newMessage(name, '已返还.')
                        where.append(w)
                        total -= 1
                        if total == 0:
                            break
                    o += 1
                if total == 0:
                    break
                w += 1
            for i in where:
                allCard[i].remove(None)

        if 1 in Skill.end:  # sakuya
            player.Player.now -= 1
            Gui.newMessage('The World!')
        Skill.end.clear()

    def init():
        Skill.function = (
            getFaith  # 0一点信仰
            ,getMoney  # 1一点钱币
            ,getRice  # 2一点粮食
            , player.Player.drawP  # 3抓一张牌
            , draw2  # 4抓2张牌
            , draw3  # 5抓3张牌
            , player.Player.exileOneP  # 6放逐手牌或弃牌堆一张
            , tongNian  # 7通念判断
            , qiaoShou  # 8巧手判断
            , appendBuff  # 9,增加buff,对于角色,在【】内+9,对于设施,在【】外+1
            , selfDestory  # 10摧毁自己
            , sanae  # 11早苗
            , suwako  # 12诹访子
            , hugeSnake  # 13巨蛇
            , minamitsu  # 14船长
            , syou  # 15寅丸星
            , kyouko  # 16幽谷响子
            , ichirin  # 17一轮
            , detector  # 18金属探测器
            , reel  # 19魔界卷轴
            , karma  # 20业障化身
            , futo  # 21物部布都
            , zombieSymbol  # 22僵尸符
            , reimu  # 23灵梦
            , kasen  # 24华扇
            , flagon  # 25萃香的酒壶
            , reisen  # 26铃仙
            , kaguya  # 27辉夜
            , gainChangeabledRes  # 28玉枝
            , roukangen  # 29楼观剑
            , foldingFan  # 30折扇
            , lostHand  # 31弃一张手牌
            , exileHand  # 32放逐一张手牌
            , stray  # 33迷途之灵
            , saigyouyou  # 34西行妖
            , alice  # 35爱丽丝
            , marisa  # 36魔理沙
            , eightTrigrams  # 37八卦炉
            , evilSpirit  # 38恶鬼
            , fireSpectre  # 39染火的怨灵
            , satori  # 40觉
            , koishi  # 41恋
            , rin  # 42燐
            , utsuho  # 43空
            , nuclearFurnace  # 44核熔炉
            , flandre  # 45芙兰
            , pachouli  # 46帕琪
            , sakuya  # 47咲夜
            , koakuma  # 48小恶魔
            , gungnier  # 49冈格尼尔
            , mouse  # 50贪吃老鼠
            , gainCenter  # 51毛玉王
            , library  # 52图书馆
            , Skill.fadeAway  # 53消逝
            , Skill.gainAnyCard  # 54 获取任意卡牌
            , appendBeliever # 55 将一张信徒放置在当前玩家牌堆顶
        )

    def fadeAway():
        '''消逝效果'''
        player.Player.exileAdd(Skill.card)
        Skill.card = None

    def spell(card):
        '''使用角色,发动设施,捕获妖怪,如果正常结束,返回默认的None'''
        Skill.card = card
        skill = card.skill
        if len(skill) == 0:
            return
        try:
            for s in skill[0]:  # 发动一个效果
                result = Skill.function[s]()
                if result != None:
                    return result
        except Exception as inst:
            # __str__ allows args to be printed directly,
            Gui.newMessage(inst)
            return None

    def retreatSkill(card):
        '''退治妖怪,设施buff'''
        Skill.card = card
        skill = card.skill
        if len(skill) < 2:
            return
        try:
            for s in skill[1]:  # 发动一个效果
                result = Skill.function[s]()
                if(result != None):
                    return result
        except Exception as inst:
            # print(type(inst))	# the exception instance
            # print(inst.args)	 # arguments stored in .args
            # __str__ allows args to be printed directly,
            Gui.newMessage(inst)
            return None

    def checkMiracle(name:str):
        '''按照名字调用相应的奇迹效果函数'''

        # 下面部分是无需通信的奇迹
        if name == '云居一轮&云山':
            miracleShuffle()
        elif name == '因幡帝':
            miracleDraw()
        elif name == '西行妖':
            saigyouyou()
        else:
            return
            # 下面部分的奇迹需要通信
            ni = NetMessage.instance
            oldState=ds.state
            ds.setWaiting(True)

            if ds.canAdd():
                # 本地操作时触发奇迹,先把前面的操作传递,然后给奇迹通信开个头,包括奇迹头部码和本地玩家序号
                afterOperation( ni.getMessage() )
                # ni.setHead('3_')
                # ni.add(Info.thisPlayer)
            else:
                # 否则设置队列为添加状态
                ds.clear()
                ds.setAdding()

            if name == '激光宝塔':
                miracleRebuild()
            elif name == '物部布都':
                miracleExile()
            elif name == '神奈子的御柱':
                miracleMissionary()

            ds.setWaiting(False)
            ds.state = oldState
            # afterOperation( ni.getMessage() )

    def checkRetreat(cost):
        '''退治妖怪时触发的效果,我觉得应当由player.Player实现...'''
        if not player.Player.timing[2]:
            return
        b = player.Player.buff
        if b[10] and player.Player.cp.haveFacility('赛钱箱'):
            Gui.newMessage('赛钱箱生效。')
            getMoney()
            player.Player.lostBuff(10)
        if b[11]:
            Gui.newMessage('宫古芳香生效。')
            player.Player.drawP(1)
            player.Player.lostBuff(11)
        if b[12]:
            Gui.newMessage('蕾米莉亚 斯卡雷特生效。')
            gainCenter(cost, [0, 1])

    def checkBeforeGain(card):
        '''判断能否获得某一张牌,包括洋馆,资源替代buff'''
        if not player.Player.timing[0]:
            return Skill.canGain(card.cost)
        if player.Player.buff[2] and card.category() == 1 and player.Player.cp.haveFacility('洋馆'):
            getMoney()
            if Skill.checkBeforeGain2(card.cost):
                Gui.newMessage('洋馆生效。')
                player.Player.lostBuff(2)
                if card.cost[1] == 0:
                    getMoney(-1)
                return True
            else:
                getMoney(-1)
                return False
        else:
            return Skill.checkBeforeGain2(card.cost)

    def checkBeforeGain2(cost):
        '''资源相互转换的buff判断,最终会将资源设置成恰好满足的情况'''
        res = player.Player.resource
        b = player.Player.buff
        result = [res[i]-cost[i] for i in range(3)]
        source = [None]*3
        # print(result)
        if b[3]:
            source[1], source[2] = 0, 0
        if b[4]:
            source[0] = 1
        if b[5]:
            source[1] = 0
        if not (b[3] or b[4] or b[5]):
            return Skill.canGain(cost)
        for i in range(3):
            if result[i] < 0:  # 找到一个资源不足的点
                if source[i] == None:  # 无来源时
                    return False
                else:  # 检查来源能否补给
                    s = source[i]
                    result[s] += result[i]
                    if result[s] < 0:
                        return False
                    else:
                        result[i] = 0
        for i in range(3):
            res[i] = cost[i]+result[i]
        return True

    def canGain(cost):
        '''最简单的比大小判断'''
        r = player.Player.resource
        for i in range(3):
            if r[i] < cost[i]:
                return False
        return True

    @whenOperateion
    def spellAny(index=None, *args):
        '''使用任一个技能'''
        NetMessage.instance.add('7_0')
        no = simpledialog.askinteger('', '请输入技能序号：')
        if no==None or no >= len(Skill.function):
            return False
        print('sepll', no,flush=1)
        Skill.function[no]()
        # return f'7_0'

    def gainAnyCard(*e):
        a = simpledialog.askinteger(
            title='获得任意一张卡牌', prompt='输入卡片的地点序号')
        if a==None:
            return False
        b = simpledialog.askinteger(
            title='获得任意一张卡牌', prompt='输入卡片的在该牌堆的编号')
        if b==None:
            return False
        card = Card.gainAnyCard(int(a), int(b))
        if card==None:
            return False
        player.Player.cp.hand.append(card)
        Gui.handAppend()


# ---------------|machining function|-----------------

def miracleDraw():  # 抽一
    Gui.newMessage('所有玩家抓一张牌。')
    for i,v in enumerate(player.Player.player):
        v.draw(1, i == player.Player.now)

def miracleShuffle():  # 洗回
    Gui.newMessage('所有玩家将弃牌堆洗回卡组。')
    for i in player.Player.player:
        i.deck += i.throw
        shuffle(i.deck)
        i.throw = []

def miracleExile():  # 放逐,
    Gui.newMessage('所有玩家可以放逐一张牌。')
    # 先询问本地的玩家的操作
    tp = Info.thisPlayer
    pls = player.Player.player
    Gui.record()
    Gui.flash(pls[tp])
    pls[tp].exileOne()

    # 通信将操作传递
    # afterOperation(NetMessage.instance.getMessage())
    ds.setGetting()
    Info.connecter.setData( Info.thisPlayer,ds.get() )
    # 接受通信后逐个复现（不重复本地玩家的）,如果还有玩家尚未选择,这里会阻塞
    for i, v in enumerate(pls):
        if i == tp:
            ds.get()
            continue
        v.exileOne()
    Gui.flash(player.Player.cp, False)

def miracleRebuild():  # 重建
    Gui.newMessage('所有玩家可以将一张弃牌堆中的设施牌加入手卡。')
    # 先询问本地的玩家的操作
    tp = Info.thisPlayer
    pls = player.Player.player
    Gui.record()
    Gui.flash(pls[tp])
    pls[tp].rebuild()

    # 通信将操作传递
    ds.setGetting()
    Info.connecter.setData(Info.thisPlayer, ds.get())
    # 接受通信后逐个复现（不重复本地玩家的）,如果还有玩家尚未选择,这里会阻塞
    for i, v in enumerate(pls):
        if i == tp:
            ds.get()
            continue
        v.rebuild()
    Gui.flash(player.Player.cp, False)

def miracleMissionary():  # 传教
    def askMission(p: player.Player):
        put = messagebox.askyesno('神奈子的御柱', '是否将一张 教徒 放置在你的牌堆顶？')
        if put:
            card = Gui.getCover(9)
            Gui.newMessage(p.name+" 选择获得一张教徒")
            p.deck.append(card)

    Gui.newMessage('所有玩家可以将一张弃牌堆中的设施牌加入手卡。')
    # 先询问本地的玩家的操作
    tp = Info.thisPlayer
    pls = player.Player.player
    Gui.record()
    Gui.flash(pls[tp])
    askMission(pls[tp])

    # 通信将操作传递
    ds.setGetting()
    Info.connecter.setData(Info.thisPlayer, ds.get())
    # 接受通信后逐个复现（不重复本地玩家的）,如果还有玩家尚未选择,这里会阻塞
    for i, v in enumerate(pls):
        if i == tp:
            ds.get()
            continue
        askMission(v)
    Gui.flash(player.Player.cp, False)

def evilSpirit():
    ask = messagebox.askyesno('恶鬼', '是否放弃摧毁设施,改为获得3点钱币？')
    if ask:
        getMoney(3)
        return
    Gui.record()
    now, total = player.Player.now, player.Player.total
    pls = player.Player.player
    r = -2
    for cur in range(total):
        if cur == now:
            continue
        l = len(pls[cur].facility)
        if(l == 0):
            Gui.newMessage(
                f'{pls[cur].name}的设施区没有设施!')
        elif l == 1:
            pls[cur].destory(0, False)
        else:
            Gui.flash(pls[cur])
            while True:
                r = Gui.askVar(1, '选择设施区内一张设施保留,然后摧毁其他设施：')
                if (r != -2):
                    break
            f = pls[cur].facility
            remain = f.pop(r)
            pls[cur].throw += f
            f = []
            f.append(remain)
            pls[cur].facility = f
            Gui.newMessage(f'{pls[cur].name}保留了{remain.name}')
            # for i in len(f):
            # 	player[cur].destory(0,False)
    Gui.flash(player.Player.cp, False)


def mouse():
    now, total = player.Player.now, player.Player.total
    pls = player.Player.player
    Gui.record()
    for cur in range(total):
        if cur == now:
            continue
        l = len(pls[cur].facility)
        if l == 0:
            Gui.newMessage(
                f'{pls[cur].name}的设施区没有设施!')
            continue
        elif l == 1:
            r = 0
        else:
            Gui.flash(pls[cur])
            while True:
                r = Gui.askVar(1, '选择设施区内一张设施摧毁：')
                if(r != -2):
                    break
        # f=pls[cur].facility.pop(r)
        # Gui.facilityLost(r)
        pls[cur].destory(r, False)
        # Gui.newMessage(f' 摧毁了{pls[cur].name}的{f.name}.')
    Gui.flash(player.Player.cp, False)


def flagon(): return resourceChange(2, 1)  # 萃香的酒壶


def kasen(): return gainChangeabledRes([0, 1], 3)  # 茨木华扇


def zombieSymbol():  # 僵尸符
    return resourceChange(2, 0)


def library(): return gainChangeabledRes([1, 2])


def reimu(): return gainCenter(20, [2])


def futo():  # 物部布都
    p = player.Player.cp
    first = False
    while True:
        no = Gui.askVar(2, '弃两张牌或者一张信仰牌')
        if(no == -2):
            continue
        p.lost(no)
        card = p.throw[-1]
        # if card.name==Skill.card.name:continue
        if(card.isFaith() or first):
            return
        else:
            first = True


def reel():  # 魔界卷轴
    if(player.Player.faithCard > 1):
        return player.Player.cp.rebuild()
    else:
        Gui.newMessage('条件不满足!')
        return 1


def detector():  # 金属探测器
    p = player.Player.cp
    if p.checkDeck():
        return 1
    else:
        card = p.deck[-1]
        Gui.explain(str(card))
        if(card.category() == 1):
            gain = messagebox.askyesno(
                '金属探测器', f'获得{card.name}?')
            if(gain):
                p.draw(1)
        else:  # not facility
            throw = messagebox.askyesno(
                '金属探测器', f'丢弃{card.name}?')
            if(throw):
                p.throw.append(p.deck.pop())
                Gui.newMessage(f'{p.name}丢弃了{card.name}')


def minamitsu():  # 村纱
    p = player.Player.cp
    f = p.facility
    l, n = len(f), 0
    while l != 0:
        no = Gui.askVar(1, '摧毁任意张设施,摸等量的牌（按 取消 键结束选择）：')
        if no == -2:
            break
        elif no < l:
            p.destory(no)
            l -= 1
            n += 1
    if n != 0:
        p.draw(n)


def syou():  # tiger
    if len(player.Player.cp.facility) == 0:
        return 0
    no = Gui.askVar(1, '摧毁设施区一张设施,获得2枚钱币')
    if(no == -2):
        return 0
    return player.Player.cp.destory(no)


def kyouko():  # 响子
    return copyChar(True)


def ichirin():  # 一轮
    card = exileCenter()
    if card == 1:
        return 1
    if card.category() == 1:
        getFaith(3)


def kaguya():
    p = player.Player.cp
    # 定好目标牌数
    if len(p.deck) < 5:
        shuffle(p.throw)
        p.throw += p.deck
        p.deck = p.throw
        p.throw = []
    n = len(p.deck)
    n = min(n, 5)
    if n == 0:
        Gui.newMessage('No card!')
        return

    card = p.deck[-n:]
    card = Gui.sort(card, '蓬莱山辉夜',
        '先选择一张加入手牌或放逐,其余排序后放回,先选择的在下：')
    choose = card.pop(0)
    add = messagebox.askyesno('蓬莱山辉夜',
        f'是否将{choose.name}加入手卡？\n若否,则将其放逐。')

    if add:
        Gui.newMessage(f'{choose.name}加入手卡')
        p.hand.append(choose)
        Gui.handAppend()
    else:
        player.Player.exileAdd(choose)

    p.deck.pop()
    p.deck[1-n:] = card


def karma():
    ask = messagebox.askyesno('业障化身', '是否放弃获得其他人手牌,改为获得3点任意相同种类资源？')
    if ask:
        t = Gui.askAType([0, 1, 2], '业障化身')
        gainResource(t, 3)
        return
    p = player.Player.player
    card = None
    h = player.Player.cp.hand
    for i in range(player.Player.total):
        if i == player.Player.now:
            continue
        p[i].neatHand()
        l = len(p[i].hand)
        if l == 0:
            Gui.newMessage(f'{p[i].name}没有手牌.')  # has no hand
            continue
        else:
            while True:
                no = randint(0, l-1)
                if p[i].hand[no] != None:
                    # 失去手牌
                    card = p[i].hand[no]
                    p[i].hand[no] = None
                    Gui.newMessage(
                        f'获得了{p[i].name}的{card.name}')
                    # 记录卡片及玩家
                    Skill.no.append(i)
                    Skill.cardTemp.append(card.name)
                    # 标记被拿走卡牌
                    # card.skill.append(10)
                    h.append(card)
                    Gui.handAppend()
                    break
    if card != None:
        Skill.end.append(0)


def foldingFan():
    no = 0
    while True:
        no = Gui.askVar(0, '选择一个中央牌堆,对其最上面三张排序')
        if no == -2:
            return 1
        elif no < 9:
            break
    Gui.center.sortThree(no)


def saigyouyou():
    Gui.newMessage('无事发生')
    return


def alice(): return


def roukangen():  # 楼观剑
    if player.Player.cp.haveFacility('白楼剑'):
        getRice()
    else:
        return 1


def stray():  # 迷途之灵
    player.Player.exileOneP()
    justExileCenter()


def eightTrigrams():
    player.Player.exileOneP()
    justExileCenter([2])


def fireSpectre():
    n = 0
    for i in player.Player.cp.monster2:
        if(i.name == '染火的怨灵'):
            n += 1
    getMoney(n)


def satori():
    pls = player.Player.player
    card, who = [], []
    for i in range(player.Player.total):
        if not pls[i].checkDeck():
            c = pls[i].deck[-1]
            Gui.newMessage(f'{pls[i].name}的牌堆顶是{c.name}.')
            if c.category() == 0:
                card.append(c)
                who.append(i)
    if card == []:
        return
    no = Gui.askOne2(card, 'satori', '选择一张复制其效果：')
    if no == -2:
        return
    # pls.Player.cp.gainResourse(card[no])
    # Skill.spell0(card[no])
    copyEffect(card[no], Skill.card)
    throw = messagebox.askyesno('satori', '是否将其丢弃？')
    if throw:
        i = who[no]
        Gui.newMessage(f'丢弃了{pls[i].name}的{card[no].name}')
        pls[i].throw.append(pls[i].deck.pop())


def koishi():
    while True:
        no = Gui.askVar(0)  # '选择中央牌堆一张牌'
        if no == -2:
            return 1
        elif no < 9:
            break
    card = Gui.getCover(no)
    if card == None:
        return 1
    
    if randint(0, 1):
        #Gui.newMessage('放逐了 古明地恋')
        Skill.fadeAway()
        Gui.newMessage(f'获得了{card.name}')
        player.Player.cp.throw.append(card)
    else:
        player.Player.exileAdd(card)
        player.Player.cp.throw.append(Skill.card)
        Skill.card = None
    Gui.nextCenter(no)


def rin():
    p = player.Player.cp
    n = -1
    card, no, name = [], [], []
    for i in p.throw:
        n += 1
        if i.category() == 0 and i.name not in name:
            card.append(i)
            no.append(n)
            name.append(i.name)
    if(card == []):
        return 1
    r = Gui.askOne2(card, 'rin', '选一张放逐或置于牌堆顶：')
    if r == -2:
        return 1
    throw = messagebox.askyesno('rin', f'是否将{name[r]}放逐？\n若否,则将其置于牌堆顶。')
    if throw:
        p.throw.pop(no[r])
        player.Player.exileAdd(card[r])
    else:
        p.deck.append(p.throw.pop(no[r]))


def nuclearFurnace():
    n = len(player.Player.cp.facility)
    getMoney(n)


def utsuho():
    n = 0
    for i in range(2):
        if(exileHand() != 0):
            n += 1
        else:
            break
    getRice(2*n)


def sakuya():  # end add 1
    money = Gui.askANumber(3, 'sakuya:',
                        '请选择你想得到的钱币的数量（最多为3）,剩余的将会变为食物：')
    if money == -2:
        return 1
    getMoney(money)
    getRice(3-money)
    if qiaoShou() == 0:
        return 0
    if messagebox.askyesno('sakuya:',
                        '是否放逐此卡,然后在回合结束后在进行一个额外回合'):
        Skill.end.append(1)
        Skill.fadeAway()
    # else:return 0
        # p.hand


def pachouli():
    if qiaoShou() == None:
        t = Gui.askAType([0, 1, 2], 'pachouli', '可以将一张人间之里牌加入手卡：')
        if t == -2:
            return
        card = Gui.getCover(t+9)
        player.Player.cp.hand.append(card)
        Gui.newMessage(f'{player.Player.cp.name}将{card.name}加入手卡.')
        Gui.handAppend()


def koakuma():
    t = Gui.askAType([0, 1, 2], 'koakuma', '可以获得一张人间之里牌：')
    if t == -2:
        return
    card = Gui.getCover(t+9)
    player.Player.cp.obtain(card)


def gungnier():
    card, name, indexs = [], [], []
    index = 0
    for i in player.Player.exile:
        if i.category() == 2 and i.name not in name:
            card.append(i)
            name.append(i.name)
            indexs.append(index)
        index += 1
    if name == []:
        Gui.newMessage('放逐区无妖怪!')
        return 1
    no = Gui.askOne2(card)
    if no == -2:
        return 1
    c = Skill.card
    player.Player.cp.obtain(card[no])
    player.Player.exile.pop(indexs[no])
    Skill.card = c


def reisen(): return copyChar()


def hugeSnake():
    p = player.Player.cp
    card = Gui.getCover(9)
    for i in range(2):
        if player.Player.exileOneP() == -2:
            return
        p.deck.append(card)


def appendBeliever():
    p=player.Player.cp
    p.deck.append(Gui.getCover(9))

def sanae():
    """ 由于早苗需要询问字符串,比较特殊,简化一下,传递和存储整数 """
    p = player.Player.cp
    if(p.checkDeck()):
        return 1

    # 如果可以取值,则取值
    isCorrect, name = None, ''
    if ds.hasVal():
        isCorrect = ds.get()
    else:
        name = simpledialog.askstring(title='Sanae', prompt='请输入你宣言的卡名:')
        Gui.newMessage(f'宣言了{name}')

    # 抽牌并确认
    p.draw()
    card = p.hand[-1]
    Gui.newMessage(f'抽到的卡为{card.name}')
    if isCorrect == None:
        isCorrect = (card != None) and (card.name == name)
        ds.add(int(isCorrect))

    # 后续处理
    if isCorrect:
        Gui.newMessage('宣言正确,获得两点信仰。')
        getFaith(2)
    else:
        Gui.newMessage('宣言错误。')


def suwako():
    while True:
        no = Gui.askVar(0, '请选择中央牌堆一张信仰牌：')
        if no == -2:
            return 1
        card = Gui.getCover(no)
        if (card.isFaith() and card.category() in [0, 1]):
            p = player.Player.cp
            if tongNian() == None:
                inTop = messagebox.askyesno(
                    'suwako', f'是否将{card.name}放置在你的牌堆顶?')
                if(inTop):
                    p.deck.append(card)
                    if player.Player.timing[1]:
                        for i in range(6, 9):
                            if player.Player.buff[i]:
                                player.Player.lostBuff(i)
                    Gui.nextCenter(no)
                    return
            p.obtain(card, no)
            return


def marisa(): return gainCenter(3, [0, 2])


def flandre(): return gainCenter(4, [1, 2])


""" ----- Rewrite function----- """


def rewrite():

    def sanae2():
        p = player.Player.cp
        if(p.checkDeck()):
            return 1
        isCorrect, name = None, ''
        if ds.hasVal():
            isCorrect = ds.get()
        else:
            name = simpledialog.askstring(title='Sanae', prompt='请输入你宣言的卡名:')
            Gui.newMessage(f'宣言了{name}')
        p.draw()
        card = p.hand[-1]
        Gui.newMessage(f'抽到的卡为{card.name}')
        if isCorrect == None:
            isCorrect = (card != None) and (card.name == name)
            ds.add(isCorrect)
        if isCorrect:
            Gui.newMessage('宣言正确,获得两点信仰。')
            getFaith(2)
        else:
            Gui.newMessage('宣言错误。')


    def miracleExile():  # 放逐,
        Gui.newMessage('所有玩家可以放逐一张牌。')
        player.Player.cp.exileOne()
        Gui.record()
        now = player.Player.now
        player = player.Player.player
        for cur in range(player.Player.total):
            if cur == now:
                continue
            Gui.flash(player[cur])
            player[cur].exileOne()
        Gui.flash(player.Player.cp, False)


    def miracleRebuild():  # 重建
        Gui.newMessage('所有玩家可以将一张弃牌堆中的设施牌加入手卡。')
        player.Player.cp.rebuild()
        now = player.Player.now
        Gui.record()
        player = player.Player.player
        for cur in range(player.Player.total):
            if cur == now:
                continue
            card, no, n = [], [], -1
            for i in player[cur].throw:
                n += 1
                if(i.category() == 1):
                    card.append(i)
                    no.append(n)
            if(no == []):
                Gui.newMessage(
                    f'{player[cur].name}弃牌堆中没有设施牌!')
                cur += 1
                continue
            elif len(no) == 1:
                r = 0
            else:
                Gui.flash(player[cur])
                r = Gui.askOne2(card)
                if(r == -2):
                    cur += 1
                    continue
            # 上手
            player[cur].hand.append(card[r])
            player[cur].throw.pop(no[r])
            Gui.newMessage(f'{player[cur].name}将{card[r].name}加入手卡.')
        Gui.flash(player.Player.cp, False)


    def miracleMissionary():  # 传教
        Gui.newMessage('所有玩家可以从中央牌堆将一张教徒放置在牌堆顶。')
        now, total = player.Player.now, player.Player.total
        card = Gui.getCover(9)
        player = player.Player.player
        put = messagebox.askyesno('神奈子的御柱', '是否将一张 教徒 放置在你的牌堆顶？')
        if put:
            Gui.newMessage(player[now].name+" 选择获得一张教徒")
            player[now].deck.append(card)
        Gui.record()
        for cur in range(total):
            if cur == now:
                continue
            Gui.flash(player[cur])
            put = messagebox.askyesno('神奈子的御柱', '是否将一张 信徒 放置在你的牌堆顶？')
            if put:
                Gui.newMessage(player[cur].name+" 选择获得一张教徒")
                player[cur].deck.append(card)
        Gui.flash(player.Player.cp, False)


    def evilSpirit():
        ask = messagebox.askyesno('恶鬼', '是否放弃摧毁设施,改为获得3点钱币？')
        if ask:
            getMoney(3)
            return
        Gui.record()
        now, total = player.Player.now, player.Player.total
        player = player.Player.player
        r = -2
        for cur in range(total):
            if cur == now:
                continue
            l = len(player[cur].facility)
            if(l == 0):
                Gui.newMessage(
                    f'{player[cur].name}的设施区没有设施!')
            elif l == 1:
                player[cur].destory(0, False)
            else:
                Gui.flash(player[cur])
                while True:
                    r = Gui.askVar(1, '选择设施区内一张设施保留,然后摧毁其他设施：')
                    if (r != -2):
                        break
                f = player[cur].facility
                remain = f.pop(r)
                player[cur].throw += f
                f = []
                f.append(remain)
                player[cur].facility = f
                Gui.newMessage(f'{player[cur].name}保留了{remain.name}')
                # for i in len(f):
                # 	player[cur].destory(0,False)
        Gui.flash(player.Player.cp, False)


    def mouse():
        now, total = player.Player.now, player.Player.total
        player = player.Player.player
        Gui.record()
        for cur in range(total):
            if cur == now:
                continue
            l = len(player[cur].facility)
            if l == 0:
                Gui.newMessage(
                    f'{player[cur].name}的设施区没有设施!')
                continue
            elif l == 1:
                r = 0
            else:
                Gui.flash(player[cur])
                while True:
                    r = Gui.askVar(1, '选择设施区内一张设施摧毁：')
                    if(r != -2):
                        break
            # f=player[cur].facility.pop(r)
            # Gui.facilityLost(r)
            player[cur].destory(r, False)
            # Gui.newMessage(f' 摧毁了{player[cur].name}的{f.name}.')
        Gui.flash(player.Player.cp, False)

    def sanae_old():
        p = player.Player.cp
        if(p.checkDeck()):
            return 1
        name = simpledialog.askstring(title='Sanae', prompt='请输入你宣言的卡名:')
        Gui.newMessage(f'宣言了{name}')
        p.draw()
        card = p.hand[-1]
        Gui.newMessage(f'抽到的卡为{card.name}')
        if(card != None and card.name == name):
            Gui.newMessage('宣言正确,获得两点信仰。')
            getFaith(2)
        else:
            Gui.newMessage('宣言错误。')

