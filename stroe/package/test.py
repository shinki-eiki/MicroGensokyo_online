#print('test.py')

#import sys
#from os import getcwd
#mainPath=sys.path[0]
from package import test1
def fun():
	print('test')

def fun2():
	#当为同级时：r'..\txt\place.txt','r'
	with open(r'.\txt\place.txt','r') as f:
		a=f.read()
		print(a)
#mainPath=getcwd()

#fun()