from tkinter import *
from tkinter.simpledialog import askstring
from tkinter import ttk

root=Tk()
w,h=256,320
#w = r.winfo_screenwidth()
#h = r.winfo_screenheight()-100
root.geometry("%dx%d+0+0" %(w,h))

def testMessage(root):
    '''测试左上角的卡牌说明框'''
    explaintion = StringVar()
    Message(root, textvariable=explaintion, relief='sunken',
         bg='grey', anchor='nw', justify='left', fg='lawngreen', font=['黑体', 16]
         ).place(relwidth=1, relheight=1)

    def change(e):
        explaintion.set(explaintion.get()+askstring(title=' ', prompt=' '))
    root.bind('<space>', change)
 
def testRadioDisable(root):
    '''结论是，button不可用时无法点击，不改变绑定变量'''
    val=IntVar(value=-1)
    def fun():
        print(val.get())
    rb=[]
    for i in range(8):
        rb.append(Radiobutton(root,variable=val,command=fun,value=i,indicatoron=0,text=str(i)))
        rb[i].pack()
        if i & 1:
            rb[i]['state'] = 'normal'
            # rb[i]['state'] = 'disable'
    
# testMessage(root)
testRadioDisable(root)

# style = ttk.Style()
# style.configure("BW.TLabel", foreground="black", background="white")

# l1 = ttk.Label(root,text="Test", style="BW.TLabel")
# l2 = ttk.Label(root,text="Test", style="BW.TLabel")
# l1.pack()
# l2.pack()
root.mainloop()


# class TestClass:
# 在修饰器函数内获取self参数的方法，其实就是实际调用时直接获取第一个参数
#     def logger(func):
#         def wrapper(*args, **kwargs):
#             print(f'function start')
#             ret = func(*args, **kwargs)
#             print(f'function end')
#             self = args【0】
#             print(self.__class__.__name__)
#             return ret
#         return wrapper
