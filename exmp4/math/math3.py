import math

n = int(input())
a = float(input())

area = (n * a * a) / (4 * math.tan(math.pi / n))

print(round(area))