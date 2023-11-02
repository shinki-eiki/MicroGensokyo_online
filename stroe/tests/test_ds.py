
# import unittest
from ..dataTransfer.dataStorage import DataStorage

ds=DataStorage()

if __name__=='__main__':
    ds.setNormal(1)    
    print(ds.get())
    
