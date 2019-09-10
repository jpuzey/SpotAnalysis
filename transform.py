import os
import math
from qgis.core import*
from shapely import affinity
import processing
from qgis.utils import iface
from qgis.core import QgsPointXY


xs = -0.0231
ys = -0.3423

xv = 0.722
yv = 0.1081

os.chdir("D:/Puzey_Lab/Merged_qgis/7.22")
print(os.getcwd())

params = {'IN': "rotated", 'DX': xs-xv, 'DY': ys-yv, 'ANGLE':0, 'SCALEX': 1, 'SCALEY': 1, 'OUT':"D:/Puzey_Lab/Merged_qgis/7.22/temp/final"}
processing.run("saga:transformvectorlayer",params)

layer = iface.addVectorLayer("D:/Puzey_Lab/Merged_qgis/7.22/temp/final.shp", "final", "ogr")
