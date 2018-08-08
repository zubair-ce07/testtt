from functools import wraps
import datetime


def validate_input(fn):
    wraps(fn)
    def case_decorator(*args, **kwargs):
        validated_input = globals()['validate_{}_args'.format(fn.__name__)](kwargs.get('year_month'))
        if not validated_input:
            return None
        kwargs['year_month'] = validated_input
        return fn(*args, **kwargs)
    return case_decorator


def validate_year(year_month):
    year = datetime.datetime.strptime(year_month, "%Y").date().strftime("%Y")
    current_year = datetime.datetime.today().year
    if int(year) <= current_year:
        return year
    return None


def validate_month(month):
    if 0 < month < 13:
        return month
    return None


def validate_year_result_args(year_month):
    try:
        if validate_year(year_month):
           return year_month
    except:
        raise ValueError("Validate input please")


def year_with_month_result_args(year_month):
    try:
        year, month = year_month.split('/')
        if validate_year(year_month) and validate_month(month):
            return {
                'year': year,
                'month': month
            }
    except:
        raise ValueError('Validate input please')


def month_bar_chart_result_args(year_month):
    return year_with_month_result_args(year_month)
