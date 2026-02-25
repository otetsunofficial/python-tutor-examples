def gen(n):
    if n > 0:
        for i in range(n):
            if i % 2 == 0:
                yield i
n = int(input())
for i in gen(n):
    print(i)