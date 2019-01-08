import re


CURRENCY_MAP = {
    '€': 'EUR',
    'EUR': 'EUR',
    '$': 'AUD',
    'AUD': 'AUD',
    'kr': 'SEK',
    'SEK': 'SEK',
}

GENDER_MAP = {
    'men': 'Men',
    'herren': 'Men',
    'women': 'Women',
    'damen': 'Women',
    'herr': 'Women',
    'dam': 'Men',
    'boy': 'Boy',
    'jungen': 'Boy',
    'girl': 'Girl',
    'mädchen': 'Girl',
    'kid': 'Unisex-Kids',
    'kinder': 'Unisex-Kids',
    'barn': 'Unisex-Kids',
    'herr, dam': 'Unisex-Adults',
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


def extract_gender(product_info):
    gender = 'Unisex-Adults'

    gender_mapped = [g_val for g_key, g_val in GENDER_MAP.items() if g_key in product_info.lower()]
    if gender_mapped:
        gender = gender_mapped[0]

    return gender
