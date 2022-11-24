import datetime

#todo create a saturday calculator
todaystr = datetime.datetime.now().strftime('%d-%m-%Y')
today = datetime.datetime.strptime(todaystr,'%d-%m-%Y')
saturday = today - datetime.timedelta(days=datetime.datetime.weekday(today)) + datetime.timedelta(days=5)
print(saturday)