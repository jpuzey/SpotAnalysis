# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:33:10 2019

@author: ywzKe
"""

'''
    This file take input of 2 sets of coordinates. 
    1 from spot 1 from vein
    then it calculates 
        1. scale -> scaling
        2. angle -> rotate
        3. difference of coordinate -> transform

'''

import os
import math
from qgis.core import*
from shapely import affinity
import processing
from qgis.utils import iface
from qgis.core import QgsPointXY



os.chdir("D:/Puzey_Lab/Merged_qgis/7.22")
print(os.getcwd())

def azimuthAngle(x1,  y1,  x2,  y2):
    angle = 0.0;
    dx = x2 - x1
    dy = y2 - y1
    if  x2 == x1:
        angle = math.pi / 2.0
        if  y2 == y1 :
            angle = 0.0
        elif y2 < y1 :
            angle = 3.0 * math.pi / 2.0
    elif x2 > x1 and y2 > y1:
        angle = math.atan(dx / dy)
    elif  x2 > x1 and  y2 < y1 :
        angle = math.pi / 2 + math.atan(-dy / dx)
    elif  x2 < x1 and y2 < y1 :
        angle = math.pi + math.atan(dx / dy)
    elif  x2 < x1 and y2 > y1 :
        angle = 3.0 * math.pi / 2.0 + math.atan(dy / -dx)
    return (angle * 180 / math.pi)


# get 2 sets of coordinates -> lines 

sc = [[0 for i in range(2)] for j in range(2)]
sc[0][0] = -0.02095
sc[0][1] = -0.40691
sc[1][0] = -0.36322
sc[1][1] = 0.52694

x1 = sc[0][0]
y1 = sc[0][1]
x2 = sc[1][0]
y2 = sc[1][1]


vc = [[0 for i in range(2)] for j in range(2)]
vc[0][0] = 0.8995
vc[0][1] = 0.278
vc[1][0] = 0.4052
vc[1][1] = 1.6444

a1 = vc[0][0]
b1 = vc[0][1]
a2 = vc[1][0]
b2 = vc[1][1]

# calculate_scaling_factor:
len_s = math.sqrt(abs((sc[1][0]-sc[0][0])**(2)+(sc[1][1]-sc[0][1])**(2)))
len_v = math.sqrt(abs((vc[1][0]-vc[0][0])**(2)+(vc[1][1]-vc[0][1])**(2)))
scafac = len_s/len_v

# change scale of vein


params = {'IN': "Vectorized", 'DX': 0, 'DY': 0, 'ANGLE':0, 'SCALEX': scafac, 'SCALEY': scafac, 'OUT':"D:/Puzey_Lab/Merged_qgis/7.22/temp/scaled"}
processing.run("saga:transformvectorlayer",params)

layer = iface.addVectorLayer("D:/Puzey_Lab/Merged_qgis/7.22/temp/scaled.shp", "scaled", "ogr")

# calculate_rotation_angle:

angle1 = azimuthAngle(x1,  y1,  x2,  y2)
angle2 = azimuthAngle(a1,  b1,  a2,  b2)

rotation = angle1-angle2

print(rotation)

params = {'IN': "scaled", 'DX': 0, 'DY': 0, 'ANGLE':rotation, 'SCALEX': 1, 'SCALEY': 1, 'OUT':"D:/Puzey_Lab/Merged_qgis/7.22/temp/rotated"}
processing.run("saga:transformvectorlayer",params)

layer = iface.addVectorLayer("D:/Puzey_Lab/Merged_qgis/7.22/temp/rotated.shp", "rotated", "ogr")
    
