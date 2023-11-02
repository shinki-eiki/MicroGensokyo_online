
# from GUI import Gui
# from player import Player

# Player.init()
# Player.player[0].showDeck()

class A():
    def fun1(self):
        print('1')

    def fun2(self):
        print('2')
    
    def __init__(self):
        self.fun=[self.fun1,self.fun2]
        
a=A()
a.fun[0]()
a.fun[1]()
