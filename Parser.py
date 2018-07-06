import datetime as dt


def parse_reading(value):
    if value in ['', '\n']:
        return None
    elif '-' in value:
        return int(value.strip()) if value[0] is '-' else dt.datetime.strptime(
            value.strip(),
            "%Y-%m-%d"
        ) if str.split(value, '-')[0].isdigit() else value
    elif value.isalpha():
        return value.strip()
    elif '.' in value:
        return float(value.strip())
    else:
        return int(value.strip())


def parse_month(string):
    parts = str.split(string, '/')
    return dt.date(int(parts[0]), int(parts[1]), 1).strftime("%B"), parts[0]
