def gen(n):
    for i in range(n):
        if i % 3 == 0 and i % 4 == 0:
            yield i
n = int(input())
for num in gen(n):
    print(num)