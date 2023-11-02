# class HomePage2():
#     '''进入游戏的开始界面,与玩家的设置界面，联网时改为'''
#     # title一直没有单独隐藏,而是随着整体隐藏,倒也无伤大雅
#     #canvas,home,title,button,choose

#     def __init__(self,r):
#         self.canvas=Label(r,bg='grey')
#         changeImageWithName(self.canvas,'homepage')
#         self.title=Label(self.canvas,text='微型\n幻想乡',font='粗体 40 bold')
#         root=self.home=Label(self.canvas,bg='palegoldenrod')

#         self.button:list[Button]=[]
#         text=['新游戏','快速开始','退出']
#         fun=[self.newGame,self.quickGame,r.quit] #self.loadGame,
#         for i in range(3):
#             self.button.append(Button(
#                 root,font='粗体 14 bold',text=text[i],command=fun[i]))
#             self.button[i].place(rely=i*0.33,relwidth=1,relheight=0.325)
#         self.title.place(relx=0.4,rely=0.1,relheight=0.2,relwidth=0.2)
#         # root.place(relx=0.4,rely=0.5,relwidth=0.2,relheight=0.42)

#         self.choose=Choose(self.canvas,self)
#         # self.choose=netUI.roomPage.RoomPage()
    
#     def newGame(self):
#         '''新游戏询问人数，然后进入设置界面'''
#         n=simpledialog.askinteger('','How many players?')
#         if not n:return
#         self.home.place_forget()
#         # self.chooseFrame.place(relx=0.2,rely=0.41,relheight=0.58,relwidth=0.5)
#         self.choose.place(n)

#     def place(self):
#         '''放置背景以及快捷按钮'''
#         self.canvas.place(relheight=1,relwidth=1)
#         self.home.place(relx=0.4,rely=0.5,relwidth=0.2,relheight=0.3)
    
#     def place_forget(self):
#         '''进入游戏时,整体隐藏'''
#         self.canvas.place_forget()

#     def quickGame(self):
#         self.place_forget()
#         Gui.gaming()
        
#     def startGame(self,name,photo,res):
#         # print('start')
#         self.place_forget()
#         Gui.gaming(name,photo,res)
#         # res=['faith','money','rice']
#         # for i in range(n):
#         # 	t=typeVar[i].get()
#         # 	print(f'Player {i+1} has no {res[t]}.')