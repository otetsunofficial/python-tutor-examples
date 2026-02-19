def generator(n):
    for i in range(n):
        yield i
n = int(input())
for num in generator(n):
    print(num)