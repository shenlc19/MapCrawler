import requests
import math
import ezdxf
import random
import time
from RequestEncoder import *
from VectorTileParser import *

z = 17 

encoded_x, encoded_y = 12950401.443563435,4839482.649214438 # 更改横纵坐标
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
dy = 4

doc = ezdxf.new()
msp = doc.modelspace()

for x in range(center_x - dx, center_x + dx):
    for y in range(center_y - dy, center_y + dy):
        # time.sleep(random.uniform(0.7, 2.5))
        myurl = geturl(x=x, y=y, z=z, styles=style, scaler=scale, showtext=showtext, udt=udt)
        response = requests.get(myurl)
        b = response.content
        offset = [(x - center_x) * 1024, (y - center_y) * 1024]
        Hc(b, msp, offset)
        print(x, ', ', y, "finished")
        
doc.saveas("output.dxf")
        