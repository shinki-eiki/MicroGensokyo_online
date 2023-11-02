from PIL import Image,ImageTk
def findhHeadImage(s):
    # a=r'..\headImage\\'+f'{s}.jpg'
    photo=ImageTk.PhotoImage(file=r'..\headImage\\'+f'{s}.jpg')
    return photo
def findImage(s='test'):#find image
    a=str(s)+'.jpg'
    photo=ImageTk.PhotoImage(file=a)
    return photo

def changeImage(label,card):
    photo=card.image
    label.config(image=photo)
    label.image=photo
# def 
def changeIma(label,name='test',place=0):
    #need to find image
    if place==0:photo=findImage(name)
    elif place==1:photo=findhHeadImage(name)
    label.config(image=photo)
    label.image=photo
def changeIma2(label,photo):
    label.config(image=photo)
    label.image=photo

import tkinter as tk
if __name__ == "__main__":
	root=tk.Tk()
	button=tk.Label(root)
	button.pack()
	changeIma(button,1)
	root.mainloop()
