'''
Created on 2013-1-17

@author: epsilon
'''
import numpy as np
from terse_proto.tsmf.model.polygon import  Polygon2D
class TestTool(object):
    @classmethod
    def wash(cls,list,time):
        for i in xrange(time):
            ri=np.random.randint(1,len(list))
            e=list[ri]
            del list[ri]
            list.append(e)
    @classmethod
    def samplePolygon(cls,coordChainsOut):
        coordChains=[[[0,0],[2,0],[2,2],[3,1],[4,2],[5,2],[3,3],[3,2],[2,4],[6,3],[7,4],[7,2],[8,5],[8,7],[7,7],[8,8],[5,9],[6,6],[5,7],[4,6],[4,8],[3,7],[2,7],[3,6],[4,4],[0,7],[2,3],[0,2]],[[5,5],[6,4],[5,4]],[[7.5,5],[7,5],[6.5,6],[7.5,6]]]
        del coordChainsOut[:]
        coordChainsOut.append(coordChains)
        return  Polygon2D(coordChainsOut)       