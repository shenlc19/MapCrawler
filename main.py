import requests
import math
import ezdxf
import random
import datetime
import sys
from RequestEncoder import *
from VectorTileParser import *

def parse_url(url):
    x, y, z = url.split("@")[1].split(",")
    x = float(x)
    y = float(y)
    z = float(z[:-1])
    return x, y, z

x, y, z = parse_url(sys.argv[1])

z = 17 

encoded_x, encoded_y = 12950401.443563435,4839482.649214438 # 更改横纵坐标
encoded_x, encoded_y = x, y
showtext = 1

m = 256 * 2 ** (18 - z)
center_x = math.floor(encoded_x / m) 
center_y = math.floor(encoded_y / m) 

scale = 2
baseunits = 256
udt = 20230724
udt = datetime.datetime.now().strftime('%Y%m%d')
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
        