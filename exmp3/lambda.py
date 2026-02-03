""""if we need to use function just once its better to use lambda func"""

numbers = [1, 2, 3, 4, 5, 6, 7, 8]
doubled = list(map(lambda x: 2 * x, numbers))
print(doubled)