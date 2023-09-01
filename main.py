import requests
import math
import ezdxf
import random
import datetime
import sys
from tqdm import tqdm
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

dx = 2
dy = 2

doc = ezdxf.new()
msp = doc.modelspace()
doc.layers.add(name='建筑物', color=2)
doc.layers.add(name='道路')

iterator = tqdm(range(dx*dy*4))
for i in iterator:
    x = center_x - dx + (i % (dx * 2))
    y = center_y - dy + (i // (dy * 2))
    
    myurl = geturl(x=x, y=y, z=z, styles=style, scaler=scale, showtext=showtext, udt=udt)
    response = requests.get(myurl)
    b = response.content
    offset = [(x - center_x) * 1024, (y - center_y) * 1024]
    Hc(b, msp, offset)
    iterator.set_description('{:d}, {:d} finished'.format(x, y))
        
doc.saveas("output.dxf")
        