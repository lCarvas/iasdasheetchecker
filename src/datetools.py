import datetime

class datetools:
    today = datetime.date.today()
    todaystr = datetime.datetime.strftime(today,'%d-%m-%Y')
    weekday = datetime.datetime.weekday(today)
    trim = (today.month - 1)//3 + 1

    @staticmethod
    def satcalc(ftoday):
        if datetools.weekday == 6:
            saturday = ftoday + datetime.timedelta(days=12-datetools.weekday)
        else:
            saturday = ftoday + datetime.timedelta(days=5-datetools.weekday)
        
        return saturday

    @staticmethod
    def trimsat():
        daylst = []
        i = datetools.today
        while(datetools.satcalc(i - datetime.timedelta(days=7)).month - 1)//3 + 1 == (datetools.today.month - 1)//3 + 1:
            i = i + datetime.timedelta(days=-7)
        while(datetools.satcalc(i).month - 1)//3 + 1 == (datetools.today.month - 1)//3 + 1:
            daylst.append(str(datetools.satcalc(i)))
            i = i + datetime.timedelta(days=7)
        
        return daylst