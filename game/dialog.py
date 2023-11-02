
import tkinter.simpledialog, tkinter.messagebox
from .con_fun import whenAsk 

# deaf 
# def beforeask(fun):
#     return fun

class simpledialog():
    """ 被修饰的对话框,包括询问整数以及字符串 """
    
    # @whenAsk
    def askstring(*arg,**kw):
        """ 未被修饰的询问字符串的对话框 """
        return tkinter.simpledialog.askstring(*arg, **kw)

    @whenAsk
    def askinteger(*arg,**kw):
        return tkinter.simpledialog.askinteger(*arg,**kw)

class messagebox():
    """ 被修饰的消息框，询问是与否 """

    @whenAsk
    def askyesno(*arg,**kw):
        return tkinter.messagebox.askyesno(*arg,**kw)
