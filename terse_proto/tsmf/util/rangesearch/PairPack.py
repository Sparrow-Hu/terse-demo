'''
Created on 2013-1-17

@author: epsilon
'''
class PairPack(object):
    def __init__(self,value,attach):
        self.key=value
        self.value=attach
        
    def getkey(self):
        return self.key
    
    def getvalue(self):
        return self.value
        