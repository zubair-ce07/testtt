
def convert_price_to_integer(price):
    return int(float(price.replace(',', ''))*100)


def pricing(prices):
    prices = set(prices)
    converted_prices = [convert_price_to_integer(price) for price in prices if price]
    converted_prices.sort()
    price_map = {
        'price': converted_prices[0]
    }
    previous_price = converted_prices[1:]
    if previous_price:
        price_map['previous_price'] = previous_price

    return price_map
