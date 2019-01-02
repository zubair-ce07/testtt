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
        prices.append(''.join(re.findall(r'\d+', record)) if record else None)

    price_details = {
        'price': prices[0],
        'previous_price': prices[1],
    }

    currency = [CURRENCY_MAP[cur] for cur in CURRENCY_MAP for rcd in price_record if rcd and cur in rcd]
    if currency:
        price_details['currency'] = currency[0]

    return price_details
