'''
Created on 2013-1-15

@author: epsilon
'''
import __builtin__
from terse_proto.tsmf.util.rangesearch.PairPack import PairPack
from terse_proto.tsmf.util.rangesearch.withpaircomparator import  WithPairComparator
from terse_proto.tsmf.util.rangesearch.DictComparator import DictComparator
class LayeredRangeTree(object):
    def __init__(self, datas, comparators, keys, values):
        if len(keys) != len(values):
            raise ValueError("Keys's size and values' size mismatch")
        keyIter = iter(keys)
        valIter = iter(values)
        pairs = []
        key = keyIter.next()
        val = valIter.next()
        pairs.append(PairPack(key, val))
        self._buildtree(comparators, datas)
        self._buildtree(comparators, pairs)
        
    @classmethod
    def factory(cls, keys, comparators):
        return LayeredRangeTree(keys, keys, comparators)
    
    def rangesearch(self, results, from_, to):
        del results[:]
        self.root.rangeQuary(results, from_, to)
        
   
    def _buildtree(self, comparators, datas):
        self.dictComparators = []
        normComps = list(comparators)
        sortedPairlists = []
        for i in xrange(len(comparators)):
            dictComparator = DictComparator(normComps, False, i)
            self.dictComparators.append(dictComparator)
            sortedPair = list(datas)
            pairComp = WithPairComparator(dictComparator)
            sortedPair.sort(cmp=pairComp.compare)
            if i == 0:
                for j in xrange(1, len(sortedPair)):
                    if 0 == pairComp.compare(sortedPair[j - 1], sortedPair[j]):
                        raise ValueError('The input data contains two elements which are indistinguishable for each other')
            sortedPairlists.append(sortedPair)
        self.root = TreeNode(sortedPairlists, 0)
        
class TreeNode(object):
    def __init__(self, outer_boss, sortedPairLists, mainKeyIndex):
        self.outer_boss = outer_boss
        sortedPs = sortedPairLists[mainKeyIndex]
        self.mainKeyIndex = mainKeyIndex
        if len(sortedPs) == 1:
            pair = sortedPs[0]
            self.key = pair.getKey()
            self.value = pair.getValue()
        else:
            midIndex = (len(sortedPs) - 1) / 2  
            pair = sortedPs[midIndex]
            self.key = pair.getKey()
            self.value = pair.getValue() 
            leftSorted = []
            rightSorted = []
            
        for i in xrange(len(sortedPairLists)):
            if i < mainKeyIndex:
                lefts = None
                rights = None 
            else:
                sortedPairs = sortedPairLists[i]
                lefts = []
                rights = []
            for p in sortedPairs:
                if self.dictComparator().compare(p.getKey(), self.key) <= 0:
                    lefts.append(p)
                else:
                    rights.append(p)
        leftSorted.append(lefts)
        rightSorted.append(rights)
        if mainKeyIndex < len(self.outer_boss.dictComparators) - 2 :
            self.associateTree = TreeNode(sortedPairLists, mainKeyIndex + 1) 
        else:
            fraCasData = FraCasData(sortedPairLists[mainKeyIndex + 1], leftSorted[mainKeyIndex + 1], rightSorted[mainKeyIndex + 1])
        left = TreeNode(leftSorted, mainKeyIndex)
        right = TreeNode(rightSorted, mainKeyIndex)
        
    def dictCompare(self, o1, o2):
        return self.dictComparator().compare(o1, o2)
    
    def isLeaf(self): 
            return self.left == None
        
    def dictComparator(self): 
            return self.outer_boss.dictComparators[self.mainKeyIndex]
        
    def getSplitNode(self, from_, to):
        v = self
        b = v.dictCompare(to, v.key) <= 0
        while not v.isLeaf() and (b or self.dictCompare(from_, v.key)) > 0:
            v = v.left if b else v.right
            b = self.dictCompare(to, v.key) <= 0
        return v
    
    def rangeQuary(self, results, from_, to):
        vs = self.getSplitNode(from_, to)
        if vs.isLeaf():
            vs.checkTo(from_, to, results)
        else :
            if self.dictComparator().getMainKey() < self.dictComparator().getKeyDimensionSize() - 2:
                v = vs.left
                while not v.isLeaf():
                    if self.dictCompare(from_, v.key) <= 0 :
                        v.right.rangeQuary(results, from_, to)
                        v = v.left
                    else :
                        v = v.right
                    
               
                v.checkTo(from_, to, results)
                v = vs.right
                while not v.isLeaf():
                    if self.dictCompare(v.key, to) <= 0:
                        v.left.rangeQuary(results, from_, to)
                        v = v.right
                    else :
                        v = v.left
                   
                
                v.checkTo(from_, to, results)
            else :
                v = vs.left
                casIndex = 0
                if not v.isLeaf():
                    casIndex = v.fraCasData.searchCasIndex(from_)
                
                while not v.isLeaf() and casIndex < v.fraCasData.keys.size():
                    if self.dictCompare(from_,v.key):
                        if v.right.isLeaf():
                            v.right.checkTo(from_, to, results)
                        else :
                            v.right.fraCasData.checkTo(results, v.fraCasData.rightCas[casIndex], to)
                       
                        casIndex = v.fraCasData.leftCas[casIndex]
                        v = v.left
                    else :
                        casIndex = v.fraCasData.rightCas[casIndex]
                        v = v.right
                   
                
                if v.isLeaf():
                    v.checkTo(from_, to, results)
                

                v = vs.right
                if not v.isLeaf():
                    casIndex = v.fraCasData.searchCasIndex(from_)
                
                while not v.isLeaf() and casIndex < v.fraCasData.keys.size():
                    if self.dictCompare(v.key,to):
                        if v.left.isLeaf():
                            v.left.checkTo(from_, to, results)
                        else :
                            v.left.fraCasData.checkTo(results, v.fraCasData.leftCas[casIndex], to)
                      
                        casIndex = v.fraCasData.rightCas[casIndex]
                        v = v.right
                    else :
                        casIndex = v.fraCasData.leftCas[casIndex]
                        v = v.left
                    
                
                if v.isLeaf():
                    v.checkTo(from_, to, results)
                    
        def checkTo(from_, to, results): 
            comparators = self.dictComparator().getComparators()
            b = True
            for i in xrange(self.mainKeyIndex, len(comparators)): 
                if comparators[i].compare(from_, self.key) > 0 or comparators[i].compare(self.key, to) > 0: 
                    b = False
                    break
                 
             
                if b :
                    results.append(self.value)
            
class FraCasData(object):
    def __init__(self, outer_boss, pairs, leftDatas, rightDatas):
        self.outer_boss = outer_boss 
        self.keys = []
        self.values = []
        for pair in pairs: 
            self.keys.append(pair.getKey())
            self.values.append(pair.getValue())
        
        self.leftCas = []
        self.rightCas = []
        l = 0
        r = 0
        for i in xrange(len(pairs)): 
            self.leftCas[i] = l
            self.rightCas[i] = r
            if l < len(leftDatas) and pairs[i] == leftDatas[l] :
                l += 1
            elif r < len(rightDatas): 
                r += 1
        
    



    def dictComparator(self):
        return self.outer_boss.dictComparators[len(self.outer_boss.dictComparators) - 1]
    
    
    def searchCasIndex(self, from_): 
        fromIndex = self.lower_bound(self.keys, from_, cmp=self.dictComparator().compare)
        if (fromIndex < 0): 
            return -fromIndex - 1
        
        return fromIndex
    def lower_bound(self, haystack, needle, lo=0, hi=None, cmp=None, key=None):
        if cmp is None: cmp = __builtin__.cmp
        if key is None: key = lambda x: x
        if lo < 0: raise ValueError('lo cannot be negative')
        if hi is None: hi = len(haystack)
    
        val = None
        while lo < hi:
            mid = (lo + hi) >> 1
            val = cmp(key(haystack[mid]), needle)
            if val < 0:
                lo = mid + 1
            else:
                hi = mid
        if val is None: return -1
        elif val == 0: return lo
        elif lo >= len(haystack): return -1 - lo
        elif cmp(key(haystack[lo]), needle) == 0: return lo
        else: return -1 - lo
    
    def checkTo(self, results, fromIndex, to): 
        comp = self.dictComparator().comparators[self.dictComparator().getMainKey()]
        for i in xrange(fromIndex, len(self.keys)):
            key = self.keys[i]
            if comp.compare(key, to) > 0: 
                return
            
            results.append(self.values[i])
             
           
        
              
    
            
                                 
    
    
        
    
              
                           
                    
            
    



