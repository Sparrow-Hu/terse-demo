'''
Created on 2013-1-17

@author: epsilon
'''
class DoubleArrayComparator(object):
    def __init__(self,compareIndex):
        self.compareIndex=compareIndex
        
    def compare(self,o1,o2):
        d1=o1[self.compareIndex]
        d2=o2[self.compareIndex]
        if d1==d2:
            return 0
        elif d1<d2:
            return -1
        else :
            return 1