
import game.GUI as gui
import game.netUI.Connecter as gnc
import game.information as gi

from time import time

timeCount=time() 

# import random
# seed=random.randint(1,1<<30)
# seed = 748218611
# random.seed(seed)
# print('Seed is', seed)

# gnc.Connecter()

# 初始页
gui.Gui.init()
gi.Info.connecter = gnc.Connecter()
print('Used time:', time()-timeCount)

# 启动服务器
# gui.Gui.homepage.newGame()
# gi.Info.connecter.connect()


gui.Gui.root.mainloop()