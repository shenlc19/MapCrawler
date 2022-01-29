import os
import requests
import time
import random
import math
from PIL import Image

encoded_x = 13524616.39584698
encoded_y = 3641198.4628604054
z = 19 #放大级别

encoded_x, encoded_y = 12957457.940399325,4824091.967998807
showtext = 1

#基本（已经实现的）接口
m = 256 * 2 ** (18 - z)
center_x = math.floor(encoded_x / m) #input("中心瓦片x坐标:")
center_y = math.floor(encoded_y / m) #input("中心瓦片y坐标:")
d_x = 12 #左右偏移量
d_y = 12 #上下偏移量
save_file_name = "小尺度"
save_file_format = ".png"


x = range(center_x - d_x, center_x + d_x)
y = range(center_y - d_y, center_y + d_y)


scale = 1
baseunits = 256
udt = 20220106
style = "pl"
ak = "8d6c8b8f3749aed6b1aff3aad6f40e37"
#style = "t%3Abuilding%7Ce%3Aall%7Cv%3Aon%7Cc%3A%23ff0000ff%2Ct%3Apoi%7Ce%3Aall%7Cv%3Aoff%2Ct%3Aroad%7Ce%3Al%7Cv%3Aoff%2Ct%3Aroad%7Ce%3Ag%7Cv%3Aon%7Cc%3A%23ff00ffff%2Ct%3Aall%7Ce%3Al%7Cv%3Aoff%2Ct%3Agreen%7Ce%3Ag%7Cc%3A%2346b316ff%2Ct%3Awater%7Ce%3Ag%7Cc%3A%230000ffff"



rows = []
for i in y:
    for j in x:
        print("downloading image (" + str(j) + "," + str(i) + ")")
        downloader = abs(i + j) % 4
        tilepath ="https://maponline{worker}.bdimg.com/tile/?qt=vtile&x={x}&y={y}&z={z}&styles={style}&udt={udt}&scaler={scaler}&showtext={showtext}".format(worker=downloader, x=j, y=i, z=z, udt=udt, scaler=scale, style=style, showtext=showtext)
        tilepath2 ="https://api.map.baidu.com/customimage/tile?&x={x}&y={y}&z={z}&udt={udt}&scale=1&ak={ak}&styles={style}]".format(x=j, y=i, z=z, udt=udt, ak=ak, style=style)
        response = requests.get(tilepath)
        
        with open(str(j) + '.png', 'wb') as f:
            f.write(response.content)
        time.sleep(random.uniform(0.2, 0.5))
    time.sleep(random.uniform(0.2, 1.2))
    new_im = Image.new('RGB', (len(x) * scale * baseunits, scale * baseunits))
    images = []
    for j in x:
        print("processing image (" + str(j) + "," + str(i) + ")")
        images.append(Image.open(str(j) + '.png'))
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += scale * baseunits
    rows.append(new_im)
    
save_im = Image.new('RGB', (len(x) * scale * baseunits, len(y) * scale * baseunits))
y_offset = (len(y) - 1) * scale * baseunits
for i in rows:
    save_im.paste(i, (0, y_offset))
    y_offset -= scale * baseunits
save_im.save(save_file_name + save_file_format)

for i in x:
    path = str(i) + '.png'
    os.remove(path)