def gen(n):
    for i in range(n):
        yield i*i
n = int(input())
for i in gen(n):
    print(i)