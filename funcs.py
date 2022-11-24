import datetime

def satcalc(ftoday,fweekday):
    if fweekday == 6:
        saturday = ftoday + datetime.timedelta(days=12-datetime.datetime.weekday(ftoday))  
    else:
        saturday = datetime.datetime.strftime(ftoday + datetime.timedelta(days=5-datetime.datetime.weekday(ftoday)), '%d-%m-%Y')
    return saturday
