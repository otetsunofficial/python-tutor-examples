from functools import reduce

numbers = [1, 2, 3, 4]
fruits = ["apple", "banana", "cherry"]
names = ["Alice", "Bob"]
ages = [25, 30]
i = 1
s = "0"

squared = list(map(lambda x: x**2, numbers))
print(squared)

even = list(filter(lambda x: x % 2 == 0, numbers))
print(even) 

sum_total = reduce(lambda x, y: x + y, numbers)
print(sum_total)

for i, fruit in enumerate(fruits):
    print(i, fruit)

for name, age in zip(names, ages):
    print(name, age)

print(type(i))
print(type(s))
print(f'"{str(i)}"')
print(f'{int(s)}')
