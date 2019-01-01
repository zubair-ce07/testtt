CURRENCY_MAP = {
    '€': 'EUR',
    'EUR': 'EUR',
    '$': 'AUD',
    'AUD': 'AUD',
    'SEK': 'SEK',
}


def extract_price_details(price_record):
    price_details = {
        'previous_price': int(float(price_record[0]) * 100) if price_record[0] else None,
        'price': int(float(price_record[1]) * 100) if price_record[1] else None,
    }

    for currency in CURRENCY_MAP:
        if currency in price_record:
            price_details['currency'] = CURRENCY_MAP[currency]

    return price_details
