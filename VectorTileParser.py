# finished
import numpy as np
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

def T(H, b, a, c):
    q = a >> 2
    f = H[q + b]
    a = 4 * (f + b + 1) + a
    p = []
    if a > c:
        return p
    for c in range(f):
        k = H[q + b + 1 + c]
        r = a + k
        p.append([a, k])
        if r % 4 != 0:
            a = r + 4 - r % 4
        else:
            a = r
    return p

def Uint32Array(b):
    ret = []
    r = list(b)
    for i in range(len(r) >> 2):
        u = r[(i << 2): (i << 2) + 4]
        u = u[0] + (u[1] << 8) + (u[2] << 16) + (u[3] << 24)
        ret.append(u)
    return ret

def Int32Array(b):
    ret = []
    r = list(b)
    for i in range(len(r) >> 2):
        u = r[(i << 2): (i << 2) + 4]
        u = u[0] + (u[1] << 8) + (u[2] << 16) + (u[3] << 24)
        if u > (1 << 31) - 1:
            u -= (1 << 32)
        ret.append(u)
    return ret

def Uint16Array(b):
    ret = []
    r = list(b)
    for i in range(len(r) >> 1):
        u = r[(i << 1): (i << 1) + 2]
        u = u[0] + (u[1] << 8)
        ret.append(u)
    return ret

# 19z building extractor
def Ub(H, b, a, c=None, q=None, f=None):
    vtx = []
    idx = []
    for k in a:
        r = k[0] >> 2
        w = H[r]
        if H[r + 1] == 8:
            k = T(H, w + 1, k[0], k[0] + k[1])
            for v in k:
                w = v[0] >> 2
                e = H[w]
                v = T(H, e + 1, v[0], v[0] + v[1])
                e = 0
                for m in v:
                    g = m[0] >> 2
                    n = H[g]
                    n = T(H, n + 1, m[0], m[0] + m[1])
                    m = Int32Array(b[n[0][0]: n[0][0] + n[0][1]])
                    l = Uint16Array(b[n[1][0]: n[1][0] + n[1][1]])
                    vtx.append(m)
                    idx.append(l)
    return vtx, idx

# road extractor
def Tb(vtx, idx, H, b, a, c, q, f, p, k):
    r = H[0]
    r = T(H, r + 1, a[0], a[0] + a[1])
    for l in r:
        A = l[0] >> 2
        B = H[A]
        l = T(H, B + 1, l[0], l[0] + l[1])
        for M in l:
            I = M[0] >> 2
            O = H[I]
            Q = T(H, O + 1, M[0], M[0] + M[1])
            M = Int32Array(b[Q[0][0]: Q[0][0] + Q[0][1]])
            J = Uint16Array(b[Q[2][0]: Q[2][0] + Q[2][1]])
            vtx.append(M)
            idx.append(J)

def GetRoads(H, b):
    h = T(H, H[1] + 2, 0, len(b))
    d = T(H, 0, h[0][0], h[0][0] + h[0][1])
    vtx, idx = [], []
    for g in d:
        l = g[0] >> 2
        u = H[l + 1]
        t = H[l + 2]
        if (u == 15):
            Tb(vtx=vtx, idx=idx, H=H, b=b, a=g, c=None, q=None, f=None, p=None, k=None)
    return vtx, idx

# convert to shapely polygon
# remember to check whether coords should be divided by 100
def ConvertToPolygonList(dt, offset=(0, 0), require_division=True):
    tile_all_polygons = []
    offset = np.array(offset)
    for v, _ in dt:
        plg = []
        v = np.array(v)
        if require_division:
            v = v / 100
        
        n_points = len(v) // 2 - 1
        st = v[:2]
        plg.append(tuple(st + offset))
        for i in range(n_points):
            mv = v[(i + 1) << 1: (i + 2) << 1]
            prev = st.copy()
            st += mv
            # msp.add_line(tuple(prev), tuple(st))
            plg.append(tuple(st + offset))
            pass
        
        plg = Polygon(plg)
        if not plg.is_valid:
            plg = plg.buffer(0)
            # print(plg.is_valid)
        tile_all_polygons.append(plg)
    
    return tile_all_polygons

# new draw function
def DrawPolygon(msp, polygon, offset=(0, 0)):
    offset = np.array(offset)
    contours = list(polygon.boundary.geoms)
    for contour in contours:
        coordinates = list(contour.coords)
        for i in range(len(coordinates) - 1):
            # delete duplicate border lines
            if ((coordinates[i][0] == coordinates[i + 1][0] and abs(coordinates[i][0]) < 1e-2) 
                or (coordinates[i][0] == coordinates[i + 1][0] and abs(coordinates[i][0] - 1024.0) < 1e-2)
                or (coordinates[i][1] == coordinates[i + 1][1] and abs(coordinates[i][1]) < 1e-2)
                or (coordinates[i][1] == coordinates[i + 1][1] and abs(coordinates[i][1] - 1024.0) < 1e-2)):
                    # print(coordinates[i], coordinates[i + 1])
                    pass
            else:
                st = tuple(np.array(coordinates[i]) + offset)
                ed = tuple(np.array(coordinates[i + 1]) + offset)
                msp.add_line(st, ed)

# ====== under construction ======
# parse a single tile
def Hc(b, msp, offset = [0, 0]):
    H = Uint32Array(b)
    # extract buildings
    h = T(H, H[1] + 2, 0, len(b))
    d = T(H, 0, h[0][0], h[0][0] + h[0][1])
    vtx, idx = Ub(H=H, b=b, a=d, c=None, q=None, f=None)
    dt = [(vtx[i], idx[i]) for i in range(len(vtx))]
    if len(dt):
        building_polygons = ConvertToPolygonList(dt)
        building_polygons = unary_union(building_polygons)
        DrawPolygon(msp, building_polygons, offset)
    vtx, idx = GetRoads(H=H, b=b)
    dt = [(vtx[i], idx[i]) for i in range(len(vtx))]
    # DrawElements(msp, dt, offset)
    if len(dt):
        road_polygons = ConvertToPolygonList(dt)
        road_polygons = unary_union(road_polygons)
        DrawPolygon(msp, road_polygons, offset)