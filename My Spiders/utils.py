FEMALE_KEYWORDS = ['women', 'woman', 'misses', 'female', 'feminine']
MALE_KEYWORDS = [' men', 'man', 'male', 'masculine']


def map_gender(raw_gender):
    raw_gender = raw_gender.lower()

    if any(gender in raw_gender for gender in FEMALE_KEYWORDS):
        return 'Women'
    elif any(gender in raw_gender for gender in MALE_KEYWORDS):
        return 'Men'

    return 'Unisex adult'


def format_price(currency, current_price, previous_price=None):
    if previous_price:
        previous_price = convert_price(previous_price)
        current_price = convert_price(current_price)

        if previous_price > current_price:

            return {
                'previous_price': previous_price,
                'current_price': current_price,
                'currency': currency
            }

        return{
            'previous_price': current_price,
            'current_price': previous_price,
            'currency': currency
        }

    return {
        'current_price': convert_price(current_price),
        'currency': currency
    }


def convert_price(price):
    return int(float(price)*100)
