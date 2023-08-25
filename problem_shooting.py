import requests
import math
import ezdxf
import random
import time
import numpy as np
from shapely import is_valid, make_valid
from shapely.geometry import Polygon, MultiPolygon, GeometryCollection, LineString
from shapely.ops import unary_union, cascaded_union

from RequestEncoder import *
from VectorTileParser import *

z = 17 

encoded_x, encoded_y = 12950418.005677607,4839668.508286618 # 更改横纵坐标
showtext = 1

m = 256 * 2 ** (18 - z)
center_x = math.floor(encoded_x / m) 
center_y = math.floor(encoded_y / m) 

scale = 2
baseunits = 256
udt = 20230724
style = "pl"
z = 19

dx = 3
dy = 3

doc = ezdxf.new()
msp = doc.modelspace()

myurl = geturl(center_x, center_y, z, styles=style, udt=udt, scaler=scale, showtext=showtext)
response = requests.get(myurl)
b = response.content
H = Uint32Array(b)
vtx, idx = GetRoads(H=H, b=b)
dt = [(vtx[i], idx[i]) for i in range(len(vtx))]

tile_all_polygons = []

for idx, (v, e) in enumerate(dt):
    # print(v)
    plg = []
    v = np.array(v) / 100
    n_points = len(v) // 2 - 1
    st = v[:2]
    plg.append(tuple(st))
    for i in range(n_points):
        mv = v[(i + 1) << 1: (i + 2) << 1]
        prev = st.copy()
        st += mv
        # msp.add_line(tuple(prev), tuple(st))
        plg.append(tuple(st))
        pass
    
    plg = Polygon(plg)
    if not plg.is_valid:
        plg = plg.buffer(0)
        # print(plg.is_valid)
    tile_all_polygons.append(plg)

    pass

# tile_all_polygons = MultiPolygon(tile_all_polygons)
# print(tile_all_polygons)
# for p in tile_all_polygons:
#     print(p)
tile_all_polygons = unary_union(tile_all_polygons)
contours = list(tile_all_polygons.boundary.geoms)
for contour in contours:
    # print(contour)
    coordinates = list(contour.coords)
    for i in range(len(coordinates) - 1):
        msp.add_line(coordinates[i], coordinates[i + 1])

doc.saveas('test.dxf')
