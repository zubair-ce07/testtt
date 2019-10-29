FEMALE_KEYWORDS = ['women', 'woman', 'misses', 'female', 'feminine']
MALE_KEYWORDS = [' men', 'man', 'male', 'masculine']


def parse_gender(raw_gender):
    raw_gender = raw_gender.lower()

    if any(gender in raw_gender for gender in FEMALE_KEYWORDS):
        return 'Women'
    elif any(gender in raw_gender for gender in MALE_KEYWORDS):
        return 'Men'

    return 'Unisex adult'


def parse_price(previous_price, current_price):
    if previous_price:
        return {
            'previous_price': int(float(previous_price)*100),
            'current_price': int(float(current_price)*100) 
        }

    return {'current_price': int(float(current_price)*100)}    
