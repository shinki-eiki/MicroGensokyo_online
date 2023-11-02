
from tkinter import Button, Frame
from tkinter.simpledialog import askinteger, askstring

from ..function import findHeadImage
from ..information import Info
# import information

def whenChange(fun):
	""" 只有修改属性后需要网络发送信息，增减是在socket里直接处理的 """
	def inner(*args, **kw):
		self = args[0]
		if not Info.isThis(self.value):
			print('非本地玩家！',flush=True)
			return
		res = fun(*args, **kw)
		if res==False:
			return
		mes=f'0_2_{res}' #0代表玩家的变化，2代表修改属性
		Info.connecter.send(mes)
		# mes：0_2_2_1_2
		# send : 玩家，属性，修改后值
	return inner
	
class PlayerLabel():
	"""将头像的label与说明文字框组合在一起，作为一个整体放置
	顺序设为昵称，头像，资源流派，索引"""

	resChar = ['★', '◎', '♨']

	def __init__(self, father, name, image, res, value):
		'''label show text'''
		kw = {
			'font': '黑体 15 bold',
			'anchor': 'nw',
			# 'state' : 'disable',
			# 'indicatoron': 0,
		}

		self.res = res  # 资源，昵称，头像
		self.name = name
		self.image = image
		self.value = value

		self.frame = Frame(father)  
		""" 包含三个控件的总控件 """
		self.resLabel = Button(self.frame, text=self.resText(),
							   command=self.changeRes, **kw)
		self.nameLabel = Button(self.frame, text=name,
								command=self.changeName, **kw)
		self.imageLabel = Button(self.frame, command=self.changeImage, **kw)
		# image = findHeadImage(image),
		self.changeImageWithPhoto( findHeadImage(image) )

		self.imageLabel.place(relheigh=1, relwidth=0.28)
		self.nameLabel. place(relx=0.3, rely=0,  relheigh=0.5, relwidth=0.70)
		self.resLabel . place(relx=0.3, rely=0.5, relheigh=0.5, relwidth=0.70)

	def resText(self) ->str:
		r=''
		for i,v in enumerate(self.resChar):
			if i==self.res:continue
			r+=v
		return r

	def setName(self,a):
		self.name = a
		self.nameLabel['text'] = a

	def setRes(self,a):
		self.res = a
		self.resLabel['text'] = self.resText()

	def setImage(self,a):
		self.image = a
		self.changeImageWithPhoto(findHeadImage(a))

	@whenChange
	def changeName(self,):
		a = askstring(title='更换昵称', prompt='请输入新昵称：')
		if a == None:
			return
		self.setName(a)
		return f'{self.value}_{0}_{a}'
	
	@whenChange	
	def changeImage(self):
		a = askinteger(title='选择头像图片', prompt='请输入头像图片的序号：')
		if a == None:
			return
		self.setImage(a)
		return f'{self.value}_{1}_{a}'

	@whenChange
	def changeRes(self,):
		a = askinteger(title='更换资源选择', prompt='请输入缺失的资源：')
		if a == None or a not in (0, 1, 2):
			print('Not correct number!')
			return
		self.setRes(a)
		return f'{self.value}_{2}_{a}'

	def changeImageWithPhoto(self, photo):
		'''use image as a parameter'''
		self.imageLabel.config(image=photo)
		self.imageLabel.image = photo

	def place(self, **kw):
		'''放置两个控件，relheight0=0.3'''
		self.frame.place(**kw)

	def place_forget(self):
		'''Hide root widgets.'''
		self.frame.place_forget()

	def setOneProperty(self,pro,res):
		if pro == 0:
			self.setName(res)
		elif pro==1:
			self.setImage(int(res))
		elif pro == 2:
			self.setRes(int(res))

	def __repr__(self) -> str:
		""" 内部存储和表示用 """
		return f'{self.name}_{self.image}_{self.res}'

	def __str__(self):
		""" 输出用 """
		return f'Name:{self.name};Resource:without {self.res};Index of image:{self.image}'

	def able(self):
		self.nameLabel['bg'] = '#E9CAA6'
		self.resLabel['bg'] = '#E9CAA6'
		# self.nameLabel['state'] = 'normal'
		# self.imageLabel['state'] = 'normal'
		# self.resLabel['state'] = 'normal'


	#---------------------------------
	def change(self, pro):
		if pro == 0:
			self.changeImage()
		elif pro == 1:
			self.changeName()
		else:
			self.changeRes()


if __name__ == '__main__':
	print('yes')
