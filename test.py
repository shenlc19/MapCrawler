import sys

# 解析网址
def parse_url(url):
    x, y, z = url.split("@")[1].split(",")
    x = float(x)
    y = float(y)
    z = float(z[:-1])
    return x, y, z

x, y, z = parse_url(sys.argv[1])
print(x, y, z)