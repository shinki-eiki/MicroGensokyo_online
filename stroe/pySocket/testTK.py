from tkinter import *

root=Tk()

class test():
    def __init__(self) -> None:
        pass
    
    def test(self):
        '''just test.'''
        print('test')

a:list[test]=[test()]
a[0].test()

for i in range(10):
    Button(root, text='test',border='1px').pack(pady=1)
    
# b=Button(root,border='1px')
# b.place(x=0,y=0,relheight=0.5,relwidth=0.5)

root.mainloop()

