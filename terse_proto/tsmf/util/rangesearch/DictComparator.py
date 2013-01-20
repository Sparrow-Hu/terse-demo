'''
Created on 2013-1-18

@author: epsilon
'''
class DictComparator(object):
    def __init__(self,comparators,copy=True,mainkey):
        if copy:
            self.comparators=list(comparators)
        else:
            self.comparators=comparators
        self.mainkey=mainkey
        
    def compare(self,o1,o2):
        for i in xrange(len(self.comparators)):
            c=self.comparators[(i+self.mainkey)%len(self.comparators)].compare(o1,o2)
            if c !=0:
                return c
            
        return 0
    
    def getslibing(self,mainkey):
        return DictComparator(self.comparators,False,mainkey)
    
    def getmainkey(self):
        return self.mainkey
    
    def getcomparators(self):
        return self.comparators
    
    def getkeyDimensionsize(self):
        return len(self.comparators)
    
        
        
        