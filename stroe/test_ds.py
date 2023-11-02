
# import unittest
from dataTransfer.dataStorage import DataStorage as ds

# ds=DataStorage()

if __name__=='__main__':
    ds.setAdding()
    ds.add(100)  
    ds.add(110)  
    ds.add(120)  
    print(ds.get())
    ds.setNormal()
    ds.show()
    print(ds.get())
    print(ds.get())
    print(ds.get())
    ds.show()
