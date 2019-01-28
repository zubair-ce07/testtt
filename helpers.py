import re


CURRENCY_MAP = {
    'GBP': 'GBP',
    'YUAN': 'YUAN',
    'SEK': 'SEK',
    'AUD': 'AUD',
    'EUR': 'EUR',
    '£': 'GBP',
    '€': 'EUR',
    '¥': 'YUAN',
    '$': 'AUD',
    'kr': 'SEK',
}

GENDER_MAP = {
    'herr, dam': 'Unisex-Adults',
    'women': 'Women',
    'female': 'Women',
    'men': 'Men',
    'herren': 'Men',
    'male': 'Men',
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
}


def extract_price_details(price_record):
    prices = []
    for record in price_record:
        price = ''.join(re.findall(r'\d+', record))
        if price:
            prices.append(int(price))

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


def extract_gender(soup):
    genders = [gender for g_key, gender in GENDER_MAP.items() if g_key in soup.lower()]
    return (genders or ['Unisex-Adults'])[0]


def item_or_request(item):
    if item['meta']['requests']:
        request = item['meta']['requests'].pop()
        request.meta['item'] = item
        yield request
    else:
        item.pop('meta')
        yield item
