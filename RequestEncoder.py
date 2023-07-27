import urllib.parse as urlparse

def parseInt(x):
    r = 0
    for i in x:
        r = r << 1
        if (i == '1'):
            r = r | 1
    return r

def EncodeParams(t):
    e = ''
    for i in t:
        n = ord(i)
        o = "{0:b}".format(n << 1)
        a = len(o)
        r = o
        if (8 > a):
            r = '0' * 8 + o
            r = r[a: a + 8]
        e += r
        
    s = 5 - (len(e) % 5)
    e = '0' * s + e
    i = 0
    h = ''
    while (i < len(e) / 5):
        num = parseInt(e[i * 5: (i + 1) * 5]) + 50
        h += chr(num)
        i += 1
    return h + str(s)

def Uint32Array(b):
    ret = []
    for i in range(len(b) >> 2):
        u = b[(i << 2): (i << 2) + 4]
        u = u[0] + (u[1] << 8) + (u[2] << 16) + (u[3] << 24)
        ret.append(u)
    return ret

def geturl(x, y, z, styles, udt, scaler, showtext):
    worker = abs(x + y) % 4
    params = "x={x}&y={y}&z={z}&styles={styles}&textimg={textimg}&scaler={scaler}&v=088&udt={udt}&json=0".format(x=x, y=y, z=z, styles=styles, textimg=showtext, scaler=scaler, udt=udt)
    url = "https://maponline{worker}.bdimg.com/pvd/?qt=vtile&param={param}".format(worker=worker, param=urlparse.quote(EncodeParams(params)))
    return url
