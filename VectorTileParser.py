import requests
H = []

def T(b, a, c):
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

url = 'https://maponline2.bdimg.com/pvd/?qt=vtile&param=A2PE%3E%3FCB8%3EE9DA%3BC8NN58%3BEL9FJE%40%3BEE%40CNHJK%3DE9GJ8J%3BEF%3EGN9%3AL%3D%3F%3ENPE4%3BEE%3E%3FBHJK%3DD9FK4%3EOCO82N5B%3BEG%3ECL5L%3ECB8%3AK52%3E%3BD8FE8FNMA%3FJPE21'
response = requests.get(url).content
b_bytelen = len(response)
r = list(response)
for i in range(len(r) >> 2):
    u = r[(i << 2): (i << 2) + 4]
    u = u[0] + (u[1] << 8) + (u[2] << 16) + (u[3] << 24)
    H.append(u)
#print(H)

h = T(H[1] + 2, 0, b_bytelen)
print(h)
d = T(0, h[0][0], h[0][0] + h[0][1])
print(d)

for i in d:
    n = i[0] >> 2
    u = H[n + 1]
    print(u)