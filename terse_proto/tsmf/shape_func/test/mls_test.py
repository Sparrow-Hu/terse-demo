'''
Created on 2013-1-6

@author: Man YUAN <epsilonyuan@gmail.com>
'''
from math import cos, sin, pi
import numpy as np
from terse_proto.tsmf.shape_func.mls import MLS
from nose.tools import ok_

def sample_interval():
    return (1.0, 4.0)

def sample_coords():
    v = np.linspace(*sample_interval())
    coords = [(x, y) for x in v for y in v]
    return coords

def polygon_xy(xy):
    x, y = xy
    val = 1.1 + 3 * x + 4.4 * y - x ** 2 - 1.3 * x * y + 2.2 * y ** 2
    val_x = 3 - 2 * x - 1.3 * y
    val_y = 4.4 - 1.3 * x + 4.4 * y
    return (val, val_x, val_y)
    
def sin_cos_xy(xy):
    cycle = 40
    par = 2 * pi / cycle
    x, y = xy
    val = sin(x * par) * cos(y * par)
    val_x = par * cos(x * par) * cos(y * par)
    val_y = -par * sin(x * par) * sin(y * par)
    return (val, val_x, val_y)

def partition_of_unity_test():
    mls = MLS()
    mls.set_diff_order(1)
    interval = sample_interval()
    v = np.linspace(*interval, num=5)
    centers = [(x, y) for x in v for y in v]
    acts = []
    coords = sample_coords()
    rad = (interval[1] - interval[0]) / 50.0 * 4
    for center in centers:
        coords_in_rad = []
        for coord in coords:
            d = np.array(coord) - center
            d = np.dot(d, d) ** 0.5
            if d <= rad:
                coords_in_rad.append(coord)
        res = mls.values(center, coords_in_rad , (rad,))
        acts.append(np.sum(res, axis=0))
    acts = np.array(acts, dtype=np.double)
    acts = abs(np.max(acts, axis=0))
    ok_(acts[0] - 1 < 1e-9)
    ok_(acts[1] < 1e-9)
    ok_(acts[1] < 1e-9)

def function_fitness_test():
    func_errors = [(polygon_xy, 1e-10), (sin_cos_xy, 1e-5)]
    
    mls = MLS()
    mls.set_diff_order(1)
    interval = sample_interval()
    v = np.linspace(*interval, num=4)
    centers = [(x, y) for x in v for y in v]
    acts = []
    coords = sample_coords()
    rad = (interval[1] - interval[0]) / 50.0 * 4
    pt_vals = np.ndarray((len(coords), 3))
    for func, err in func_errors:
        i = 0
        for coord in coords:
            val = func(coord)
            pt_vals[i] = val
            i += 1
        
        
        for center in centers:
            coords_in_rad = []
            indes = []
            i = 0
            for coord in coords:
                d = np.array(coord) - center
                d = np.dot(d, d) ** 0.5
                if d <= rad:
                    coords_in_rad.append(coord)
                    indes.append(i)
                i += 1
            res = mls.values(center, coords_in_rad , (rad,))
            
            act_val = np.dot(res[:, 0], pt_vals[indes, 0])
            act_val_x = np.dot(res[:, 1], pt_vals[indes, 0])
            act_val_y = np.dot(res[:, 2], pt_vals[indes, 0])
            acts = np.array((act_val, act_val_x, act_val_y), dtype=np.double)
            exps = np.array(func(center), dtype=np.double)
            max_err = np.max(np.abs(acts - exps))
            ok_(max_err < err, str(func) + "acts:" + str(acts) + " exps:" + str(exps) + " center:" + str(center) + "max_err:"+str(max_err)+" err_lim:" + str(err))
    


