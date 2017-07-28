
def check_leap_year(year):
    if year % 100 == 0:
        if year % 4 == 0 and year % 400 == 0:
            return True
        return False
    elif year % 4 == 0:
        return True
    return False


def days_between_dates(year1, month1, day1, year2, month2, day2):

    days_tilll_month1 = 0
    days_tilll_month2 = 0
    monthsDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for i in range(month1 - 1):
        days_tilll_month1 = days_tilll_month1 + monthsDays[i]

    for i in range(month2 - 1):
        days_tilll_month2 = days_tilll_month2 + monthsDays[i]

    days = (year2 - year1) * 365 + days_tilll_month1 + days_tilll_month2 + day2 - day1

    year_temp = year1

    while year_temp < year2+1:
        if check_leap_year(year_temp):
            days += 1
            year_temp += 1
        else:
            year_temp += 1

    if check_leap_year(year1):
        if month1 > 2:
            days -= 1
    if check_leap_year(year2):
        if month2 < 3:
            days -= 1

    return days

day = days_between_dates(2011,1,1,2012,8,8)


def test():
    test_cases = [((2012,1,1,2012,2,28), 58),
                  ((2012,1,1,2012,3,1), 60),
                  ((2011,6,30,2012,6,30), 366),
                  ((2011,1,1,2012,8,8), 585 ),
                  ((1900,1,1,1999,12,31), 36523)]
    for (args, answer) in test_cases:
        result = days_between_dates(*args)
        if result != answer:
            print "Test with data:", args, "failed"
        else:
            print "Test case passed!"


test()
