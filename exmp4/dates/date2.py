from datetime import datetime, timedelta
today = datetime.now()
yesterday = today - timedelta(days = 1)
tommorow = today + timedelta(days = 1)
print(yesterday)
print(today)
print(tommorow)