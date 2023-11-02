
from tkinter import Frame

from .playerLabel import PlayerLabel
from ..information import Info
# import information 


class Room:
	""" 房间人员信息框体，用于玩家标签的放置 """
	
	def __init__(self, root , father):
		""" root一般是窗体，father是上级类 """
		self.father=father
		self.label=Info.playerLabelList

		""" 玩家标签的列表 """
		Info.removeCount = 0
		""" 已退出的人数，想了一下，还是弃用吧 """
		self.total=0
		""" 房间内总的人数 """
		self.maxRow = 7
		""" 每列放置的标签数量最大值 """
		self.frame=root
		""" 新建一个框体作为容器（暂时不用 """
		# self.frame=Frame(root,bg='lightgrey')
		# self.frame.place(relwidth=1,relheight=1)

	def add(self, name=None, image=None,res=None,):
		""" 房间添加一个新玩家 """
		if name==None:
			name, image, res,= self.getDefaultInfo()
		self.label.append(PlayerLabel(self.frame,name,image,res,self.total))
		self.place(self.total) #-Info.removeCount)
		self.total += 1
		self.father.newMessage(f'玩家{name}进入房间。')

	def remove(self,a):
		""" 移除序号为a的玩家，从PL中移除，然后将其之后的玩家前置且value减一 """
		self.label[a].place_forget()
		name = self.label[a].name
		self.label.pop(a)
		Info.removeCount+=1
		if Info.thisPlayer>a:
			Info.thisPlayer-=1
		self.total-=1
		for i in range(a,len(self.label)):
			self.place(i)
			self.label[i].value-=1
		self.father.newMessage(f'玩家{name}退出房间。')

	def setOneProperty(self,pl,pro,res):
		""" 设置某玩家的某个属性
		pl：玩家索引；pro：属性标号；res：修改后的结果
		  """
		p = self.label[pl]
		p.setOneProperty(pro,res)
		self.father.newMessage(f'玩家{p.name}修改信息。')

	def place(self,a):
		""" 根据索引将其放置在合适位置 """
		position={'relx':0,'rely':a%self.maxRow*0.135,'relheight':0.13,'relwidth':0.48}
		if a>=self.maxRow:
			position['relx']=0.5
		self.label[a].place(**position)
	
	def clear(self):
		""" 清空房间信息 """
		Info.removeCount=self.total=0
		for i in self.label:
			i.place_forget()
		self.label.clear()

	def getDefaultInfo(self):
		""" 返回默认信息配置 """
		c=self.total
		return [ Info.defaultName[c%6]+str(c),c%10,c%3 ]
	
	#---------------------暂时用不上--------------------------------

	def addList(self, pl):
		""" 用于连接上服务器时，添加房间列表里的玩家标签 """
		for i in pl:
			self.add(*i)

	def change(self, i, pro):
		self.label[i].change(pro)
		self.father.newMessage(f'玩家{self.label[i].name}修改信息。')

if __name__=='__main__':
	from tkinter import *
	from tkinter.simpledialog import askstring
	from tkinter import ttk

	root=Tk()
	w,h=300,320
	#w = r.winfo_screenwidth()
	#h = r.winfo_screenheight()-100
	root.geometry("%dx%d+0+0" %(w,h))
	name=['reimu','marisa','youmu','sakuya','sanae','aya']
	cnt=0

	r=Room(root)
	def add(*e):
		r.add(name[cnt],cnt,cnt)
		cnt += 1
	root.bind('<Control-a>', add)
	root.mainloop()