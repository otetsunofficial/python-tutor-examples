from re import *

with open('raw.txt', 'r', encoding='utf-8') as file:
    content = file.read()

def extrct_price(text):
    pattern = r"Стоимость\s+([\d\s]+,\d{2})"
    prices = findall(pattern, text)
    return prices
def extrct_names(text):
    pattern = r"\d+\.\s*\n?(.+?)\n"
    names = findall(pattern, text, DOTALL)
    return names
print(extrct_names(content))


