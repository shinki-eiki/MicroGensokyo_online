
import unittest
from dataTransfer.dataStorage import DataStorage 


class TestDataStorage(unittest.TestCase):
    def test_init(self):
        ds = DataStorage()
        ds.add(1)
        self.assertEqual(ds.get(),1)


if __name__=='__main__':
    print('begin:')
    # unittest.test()