def gen(a, b):
    for i in range(a, b):
        yield pow(i, 0.5)
a = int(input())
b = int(input())
for num in gen(a, b):
    print(num)