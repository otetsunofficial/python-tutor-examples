"""if you experiencing problems with count of your parameters you can use args"""

def numbers(*nums):
    sum = 0
    for i in nums:
        sum += i 
    return sum
print(numbers(1,3,4,5,5,6,6,6,6,6,5,5,5,5,55,44,445,45))