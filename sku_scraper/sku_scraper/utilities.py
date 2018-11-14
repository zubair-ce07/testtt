
def convert_price_to_integer(price):
    price = remove_non_numerics(price)
    return int(float(price)*100)


def pricing(prices):
    converted_prices = [convert_price_to_integer(price) for price in set(prices) if price]
    converted_prices.sort()
    price_map = {
        'price': converted_prices[0]
    }
    previous_price = converted_prices[1:]
    if previous_price:
        price_map['previous_price'] = previous_price

    return price_map


def remove_non_numerics(price):
    return ''.join(p for p in price if p.isdigit() or p == '.')


def map_currency_code(currency_code):
    currencies = {
        '$': 'USD',
        '€': 'EUR',
        '¥': 'YEN',
        '₨': 'PKR',
        '£': 'GBP'
    }
    return currencies[currency_code]