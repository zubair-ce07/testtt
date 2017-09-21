import re


currency = {
    'R$': 'BRL',
    '€': 'EURO'
}


def clean_price(raw_price, price_regex):
    price = re.findall(price_regex, raw_price)[0]
    return price


def currency_unit(price, point):
    return int(float(price.replace(point, '.')) * 100)


def currency_information(amount):
    for symbol, name in currency.items():
        if symbol in amount:
            return name


def pricing(prices, regex, comma, point):
    if prices:
        price = sorted([currency_unit(clean_price(price, regex).replace(comma, ''), point) for price in prices])
        return {
            'price': price[0],
            'previous_price': price[1:],
            'currency': currency_information(prices[0])
        }


def is_care(care, senetence):
    return any(c in senetence for c in care)
