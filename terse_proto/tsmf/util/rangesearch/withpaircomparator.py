'''
Created on 2013-1-17

@author: epsilon
'''
class WithPairComparator(object):
    def __init__(self,comparator):
        self.comparator=comparator
        
    def compare(self,o1,o2):
        return self.compare(o1.gekey(), o2.getkey())#o1,o2有问题？难道是PairPack的实例？