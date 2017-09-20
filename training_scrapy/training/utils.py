import re


def clean_and_convert_price(raw_price, currency_conversion_rate):
    if currency_conversion_rate:
        price_regex = '\d+\.?\d*|$'
        price = re.findall(price_regex,raw_price)[0]
        return str(int(price) * currency_conversion_rate) if price else '0'
    return '0'

def currency_information(amount):
    currency = {
        'R$': ('BRL', 100),
        '€': ('EURO', 100)
    }

    for symbol, information in currency.items():
        if symbol in amount:
            return information
    return (None, None)
