

from tkinter import *
from tkinter.simpledialog import askinteger

from game.information import Info
from game.netUI.room import Room

root = Tk()
w, h = 520, 540
root.geometry("%dx%d+0+0" % (w, h))

r = Room(root, None)

root.geometry("%dx%d+0+0" % (w, h))

name = ['reimu', 'marisa', 'youmu', 'sakuya', 'sanae', 'aya']
cnt = 0

def add(*e):
    global cnt
    # r.add(name[cnt%6], cnt, cnt%12)
    r.add()
    cnt += 1

def remove(*e):
    t = askinteger(title='Which one?', prompt='The index:')
    if t!=None:
        r.remove(t)

def change(*e):
    i=askinteger('','Who?')
    t=askinteger(title='Which property?',prompt='The code:')
    if t!=None:
        r.change(i,t)

def collect(*e):
    print(*Info.getPlayerInfo())

for i in range(7):add()

Info.setThis(3)
root.bind('<Control-a>', add)
root.bind('<Control-r>', remove)
root.bind('<Control-c>', change)
root.bind('<Control-g>', collect)
root.mainloop()
