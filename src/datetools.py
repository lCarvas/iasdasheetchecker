from datetime import date, timedelta


class DateTools:
    today: date = date.today()
    weekday: int = date.weekday(today)
    trim: int = (today.month - 1) // 3 + 1

    @staticmethod
    def satcalc(ftoday: date) -> date:
        """Calculates the date of the closest Saturday to the desired date

        Args:
            ftoday (date): Date to use
        """
        if DateTools.weekday == 6:
            saturday: date = ftoday + timedelta(days=12 - DateTools.weekday)
        else:
            saturday = ftoday + timedelta(days=5 - DateTools.weekday)

        return saturday

    @staticmethod
    def trimsat() -> list[str]:
        """Returns a list with the dates of all Saturdays in the current trimester in string form"""
        daylst: list[str] = []
        i: date = DateTools.today
        while (DateTools.satcalc(i - timedelta(days=7)).month - 1) // 3 + 1 == (
            DateTools.today.month - 1
        ) // 3 + 1:
            i = i + timedelta(days=-7)
        while (DateTools.satcalc(i).month - 1) // 3 + 1 == (
            DateTools.today.month - 1
        ) // 3 + 1:
            daylst.append(str(DateTools.satcalc(i)))
            i = i + timedelta(days=7)

        return daylst
