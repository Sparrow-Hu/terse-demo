'''
Created on 2013-1-15

@author: Man YUAN <epsilonyuan@gmail.com>

@author: Sparrow HU <huhao200709@163.com>
'''

from terse_proto.tsmf.model.node import Node
import numpy as np       
            
class Segment2D(object):
    def __init__(self, point=None):
        self.head = Node(point)
        self.pred = None
        self.succ = None
    def r(self):
        return self.succ.head
    rear = property(r)
    
    def distance_to(self, xy):
        v1 = self.head.coord
        v2 = self.rear.coord
        v_e = v2 - v1
        len_e = np.dot(v_e, v_e) ** 0.5
        v_xy = xy - v1
        nv_e = v_e / len_e
        dt = np.dot(nv_e, v_xy)
        if dt >= len_e:
            return np.dot(dt, dt) ** 0.5
        elif dt <= 0:
            return np.dot(v_xy, v_xy) ** 0.5
        else:
            return abs(np.cross(v_e, v_xy))
        
    def length(self):
        x, y = self.head.coord - self.rear.coord
        return (x ** 2 + y ** 2) ** 0.5
    
    def midpoint(self):
        midpoint = (self.head.coord + self.rear.coord) / 2
        return midpoint
            
if __name__ == '__main__':
    pg = Polygon2D([[[-1, -1], [1, -1], [1, 1], [-1, 1]],
                     [[-0.5, -0.5], [-0.5, 0.5], [0.5, 0.5], [0.5, -0.5]]])
    print pg.chains_heads[0].midpoint()
    #print Segment2D([-1, -1]).midpoint()
    
        
