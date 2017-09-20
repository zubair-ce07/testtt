import re


currency = {
    'R$': 'BRL',
    '€': 'EURO'
}


def clean_price(raw_price, price_regex):
    price = re.findall(price_regex, raw_price)[0]
    return int(float(price) * 100)


def currency_information(amount):
    for symbol, name in currency.items():
        if symbol in amount:
            return name


def pricing(response, price_css, price_regex):
    product_price = response.css(price_css).extract()
    if product_price:
        currency = currency_information(product_price[0])
        price = sorted([clean_price(price, price_regex) for price in product_price])
        return {
            'price': price[0],
            'previous_price': price[1:],
            'currency': currency
        }


def is_care(care, string):
    return any(c in string.lower() for c in care)
