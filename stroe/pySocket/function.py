from PIL import Image,ImageTk

# imgOpen=Image.open(a)
# photo=ImageTk.PhotoImage(imgOpen)
# return photo
def testPrint(*s):
    for i in s:print(s)

def findHeadImage(s):
    '''头像文件夹下'''
    a='headImage/'+f'{s}.jpg'
    imgOpen=Image.open(a)
    photo=ImageTk.PhotoImage(imgOpen)
    return photo

def findImage(s='test'):#find image
    '''#当前目录下'''
    a=str(s)+'.jpg'
    photo=ImageTk.PhotoImage(file=a)
    return photo

def findCardImage(s='test'):#find image
    '''#image文件夹下'''
    a='image/'+f'{s}.jpg'
    photo=ImageTk.PhotoImage(file=a)
    return photo

def changeImageWithCard(label,card):
    '''#给出card对象'''
    photo = card.getImage()
    label.config(image=photo)
    label.image=photo
# 
def changeImageWithName(label,name='cover',place=0):
    '''#place indicate where the image is,0 is root directory,and 1 is headImage'''
    #need to find image
    if place==0:photo=findImage(name)
    elif place==1:photo=findHeadImage(name)
    label.config(image=photo)
    label.image=photo

#给出图片
def changeImageWithPhoto(label,photo):
    label.config(image=photo)
    label.image=photo

# import tkinter as tk
# if __name__ == "__main__":
# 	root=tk.Tk()
# 	button=tk.Label(root)
# 	button.pack()
# 	changeIma(button,1,1)
# 	root.mainloop()
