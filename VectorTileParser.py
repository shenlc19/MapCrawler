# finished
import numpy as np

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

def DrawElements(msp, dt, offset = [0, 0]):
    edges = {}
    tmp_offset = np.array(offset)
    for v, e in dt:
        x = []
        tmp = np.array([0, 0])
        # x.append(tmp)
        for j in range(len(v) // 2):
            xi = np.array(v[j * 2: j * 2 + 2])
            tmp = tmp + xi
            # print(tmp)
            x.append(tmp / 100 + tmp_offset)
            
        # print(x)
        # print(e)
        for j in range(len(e) // 3):
            # print (e[j * 3], e[j * 3 + 1])
            # print((x[e[j * 3]][0], x[e[j * 3]][1]), (x[e[j * 3 + 1]][0], x[e[j * 3 + 1]][1]))
            e1 = ((x[e[j * 3]][0], x[e[j * 3]][1]), (x[e[j * 3 + 1]][0], x[e[j * 3 + 1]][1]))
            e2 = ((x[e[j * 3 + 2]][0], x[e[j * 3 + 2]][1]), (x[e[j * 3 + 1]][0], x[e[j * 3 + 1]][1]))
            e3 = ((x[e[j * 3]][0], x[e[j * 3]][1]), (x[e[j * 3 + 2]][0], x[e[j * 3 + 2]][1]))
            e1 = (sorted(e1)[0], sorted(e1)[1])
            e2 = (sorted(e2)[0], sorted(e2)[1])
            e3 = (sorted(e3)[0], sorted(e3)[1])
            if e1 in edges:
                edges[e1] += 1
            else:
                edges[e1] = 1
            if e2 in edges:
                edges[e2] += 1
            else:
                edges[e2] = 1
            if e3 in edges:
                edges[e3] += 1
            else:
                edges[e3] = 1
    for edge in edges:
        if edges[edge] == 1:
            msp.add_line(edge[0], edge[1])

# ====== under construction ======
def Hc(b, msp, offset = [0, 0]):
    H = Uint32Array(b)
    # extract buildings
    h = T(H, H[1] + 2, 0, len(b))
    d = T(H, 0, h[0][0], h[0][0] + h[0][1])
    vtx, idx = Ub(H=H, b=b, a=d, c=None, q=None, f=None)
    dt = [(vtx[i], idx[i]) for i in range(len(vtx))]
    DrawElements(msp, dt, offset)
    vtx, idx = GetRoads(H=H, b=b)
    dt = [(vtx[i], idx[i]) for i in range(len(vtx))]
    DrawElements(msp, dt, offset)