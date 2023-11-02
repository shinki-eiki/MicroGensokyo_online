

from tkinter import Radiobutton,Entry,messagebox,Button,END
from tkinter.scrolledtext import ScrolledText

class ChatBox:
    def __init__(self,root) -> None:
        self.build(root)
    
    def build(self,root):
        self.mes = ScrolledText(root,undo=True, fg='lightgreen', cursor='pencil',
            font='黑体 13', bg='grey')
        self.text=Entry(root)
        self.button=Button(root,text='Send',command=self.sendMessage)
        #place
        self.mes.place(relx=0,rely=0,relheight=0.78,relwidth=1)
        self.text.place(relx=0.8,rely=0,relheight=0.2,relwidth=0.78)
        self.button.place(relx=0.8,rely=0.8,relheight=0.2,relwidth=0.2)
    
    def sendMessage(self):
        # 接受输入框内的信息，发送，然后清空
        t=self.text.get()
        print('send:',t)
        # self.text.delete()
        

    def newMessage(self,text):
        # 接收新信息并显示
        self.mes.insert(END, text)
        self.mes.see(END)
                
