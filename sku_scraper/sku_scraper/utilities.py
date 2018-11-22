
currency_map = {
    '$': 'USD',
    '€': 'EUR',
    '¥': 'YEN',
    '₨': 'PKR',
    '£': 'GBP'
}


gender_map = {
    'women': 'Women',
    'men': 'Men',
    'female': 'Women',
    'male': 'Men',
    'kids': 'Kids',
    'boy': 'Kids',
    'girl': 'Kids',
    'unisex': 'Unisex'
}


merch_info_map = {
    'limited': 'Limited Edition',
    'special': 'Special Edition'
}


def convert_price_to_integer(price):
    if price:
        return int(float(price) * 100)


def pricing(soup):
    prices = remove_non_numerics(soup)
    converted_prices = [convert_price_to_integer(price) for price in set(prices) if price]
    converted_prices.sort()

    price_map = {
        'price': converted_prices[0]
    }
    previous_price = converted_prices[1:]
    if previous_price:
        price_map['previous_price'] = previous_price

    price_map['currency'] = extract_currency(soup)
    return price_map


def remove_non_numerics(raw_prices):
    return [''.join(p for p in price if p.isdigit() or p == '.') for price in raw_prices if price]


def detect_currency(currency_code):
    return currency_map.get(currency_code)


def detect_merch_info(soup):
    for merch_info in merch_info_map.keys():
        if merch_info in soup.lower():
            return merch_info_map.get(merch_info)


def detect_gender(soup):
    for gender in gender_map.keys():
        if gender in soup:
            return gender_map.get(gender, 'unisex-adults')


def extract_currency(money_strings):
    if isinstance(money_strings, list):
        money_string = ' '.join(m_str for m_str in money_strings if m_str)
    for char in money_string:
        currency = detect_currency_code(char)
        if currency:
            return currency
