from datetime import datetime

def format_date(date, date_format):
    return datetime.strptime(date, date_format).date()
