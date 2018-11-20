
def convert_price_to_integer(price):
    if price:
        return int(float(price)*100)


def pricing(raw_prices):
    prices = remove_non_numerics(raw_prices)
    converted_prices = [convert_price_to_integer(price) for price in set(prices) if price]
    converted_prices.sort()

    price_map = {
        'price': converted_prices[0]
    }
    previous_price = converted_prices[1:]
    if previous_price:
        price_map['previous_price'] = previous_price

    price_map['currency'] = extract_currency(raw_prices)
    return price_map


def remove_non_numerics(raw_prices):
    return [''.join(p for p in price if p.isdigit() or p == '.') for price in raw_prices if price]


def map_currency_code(currency_code):
    currencies = {
        '$': 'USD',
        '€': 'EUR',
        '¥': 'YEN',
        '₨': 'PKR',
        '£': 'GBP'
    }
    return currencies.get(currency_code)


def map_merch_info(item_details):
    merch_info_map = {
        'limited': 'Limited Edition',
        'special': 'Special Edition'
    }
    for merch_info in merch_info_map.keys():
        if merch_info in item_details.lower():
            return merch_info_map.get(merch_info)


def map_gender(raw_string):
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

    for gender in gender_map.keys():
        if gender in raw_string:
            return gender_map.get(gender, 'unisex-adults')


def extract_currency(money_strings):
    if isinstance(money_strings, list):
        money_string = ' '.join(m_str for m_str in money_strings if m_str)
    for char in money_string:
        currency = map_currency_code(char)
        if currency:
            return currency
 