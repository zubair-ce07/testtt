import re


CURRENCY_MAP = {
    '€': 'EUR',
    'EUR': 'EUR',
    '$': 'AUD',
    'AUD': 'AUD',
    'kr': 'SEK',
    'SEK': 'SEK',
}


def extract_price_details(price_record):
    prices = []
    for record in price_record:
        price = ''.join(re.findall(r'\d+', record))
        if price:
            prices.append(price)

    prices.sort()
    price_map = {}
    price_map['price'], *previous_price = prices
    if previous_price:
        price_map['previous_price'] = previous_price

    price_soup = ' '.join(price_record)
    currency = [c for c_key, c in CURRENCY_MAP.items() if c_key in price_soup]
    if currency:
        price_map['currency'] = currency[0]

    return price_map
