def clean_price(raw_price):
    price = ''
    for digit in raw_price:
        if digit.isnumeric():
            price += digit
    return price

def currency_name(amount):
    currency = {
        'R$': 'BRL'
    }

    for symbol, name in currency.items():
        if symbol in amount:
            return name
    return None