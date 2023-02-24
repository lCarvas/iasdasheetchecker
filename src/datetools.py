import datetime

class datetools:
    today = datetime.datetime.strptime(datetime.datetime.now().strftime('%d-%m-%Y'),'%d-%m-%Y')
    todaystr = datetime.datetime.strftime(today,'%d-%m-%Y')
    weekday = datetime.datetime.weekday(today)

    @staticmethod
    def satcalc(ftoday,fweekday):
        if fweekday == 6:
            saturday = datetime.datetime.strftime(ftoday + datetime.timedelta(days=12-datetime.datetime.weekday(ftoday)), '%d-%m-%Y')  
        else:
            saturday = datetime.datetime.strftime(ftoday + datetime.timedelta(days=5-datetime.datetime.weekday(ftoday)), '%d-%m-%Y')
        
        return saturday

    @staticmethod
    def trimsat():
        daylst = []
        i = datetools.today
        while (int(str(datetools.satcalc(i,datetools.weekday))[3:5]) - 1)//3 + 1 == (int(datetools.todaystr[3:5]) - 1)//3 + 1:
            daylst.append(datetools.satcalc(i,datetools.weekday))
            i = i + datetime.timedelta(days=7)
        daylst.reverse()
        
        return daylst