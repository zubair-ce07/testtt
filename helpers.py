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
    prices_map = []

    for record in price_record:
        price = ''.join(re.findall(r'\d+', record))
        if price:
            prices_map.append(price)

    prices_map.sort()
    price_details = {}
    price, *previous_price = prices_map
    price_details['price'] = price
    if previous_price:
        price_details['previous_price'] = previous_price

    currency = [CURRENCY_MAP[cur] for cur in CURRENCY_MAP for rcd in price_record if rcd and cur in rcd]
    if currency:
        price_details['currency'] = currency[0]

    return price_details
