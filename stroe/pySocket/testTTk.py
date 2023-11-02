from tkinter import *
from tkinter import ttk

root=Tk()
style = ttk.Style()
style.configure("BW.TLabel", foreground="black", background="white")

l1 = ttk.Label(root,text="Test", style="BW.TLabel")
l2 = ttk.Label(root,text="Test", style="BW.TLabel")
l1.place(x=0,y=0,relheight=0.5,relwidth=0.5)

root.mainloop()

