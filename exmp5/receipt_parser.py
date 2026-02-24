from re import *
import json

with open('raw.txt', 'r', encoding='utf-8') as file:
    content = file.read()

def extract_price(text):
    pattern = r"Стоимость\s+([\d\s]+,\d{2})"
    prices = findall(pattern, text)
    return prices
def extract_names(text):
    pattern = r"\d+\.\s*\n(.+?)\n\d+[,.\d\s]+\s*x\s*[\d\s,]+\n[\d\s,]+\nСтоимость"
    names = findall(pattern, text, DOTALL)
    return names
def calculate_total(text):
    prices = extract_price(text)
    total = 0
    for i in prices:
        num = float(i.replace(" ", "").replace(",","."))
        total += num
    return total
def extract_date_time(text):
    pattern = r"Время:+\s*(.+?)\n"
    date_time = findall(pattern, text, DOTALL)
    return date_time
def extract_payment_method(text):
    pattern = r"([^\n]+)\n[^\n]+\nИТОГО:"
    payment_method = findall(pattern, text, DOTALL)
    return payment_method

names = extract_names(content)
prices = extract_price(content)
total = calculate_total(content)
date_time = extract_date_time(content)
payment_method = extract_payment_method(content)

json_dict = {
    "items": [
        {
            "name": name.strip(),
            "price": float(price.replace(" ", "").replace(",", "."))
        }
        for name, price in zip(names, prices)
    ],
    "total_amount": total,
    "date": date_time[0] if date_time else None,
    "payment_method": payment_method[0].rstrip(":") if payment_method else None
}

print(json.dumps(json_dict, ensure_ascii=False, indent=4))


