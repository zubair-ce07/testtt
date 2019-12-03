from enum import Enum


class Gender(Enum):
    MEN = 'men'
    WOMEN = 'women'
    GIRLS = 'girls'
    BOYS = 'boys'
    KIDS = 'unisex-kids'
    ADULTS = 'unisex-adults'


GENDER_MAP = {
    'menswear': Gender.MEN.value,
    'dads': Gender.MEN.value,
    'dad': Gender.MEN.value,
    'mom': Gender.WOMEN.value,
    'womans': Gender.WOMEN.value,
    'mans': Gender.MEN.value,
    'lady': Gender.WOMEN.value,
    'shopbyproductladies': Gender.WOMEN.value,
    'male': Gender.MEN.value,
    'female': Gender.WOMEN.value,
    'babys': Gender.KIDS.value,
    'beauty': Gender.WOMEN.value,
    'babies': Gender.KIDS.value,
    'clutches': Gender.WOMEN.value,
    'kidswear': Gender.KIDS.value,
    'boyfriend': Gender.WOMEN.value,
    'womens': Gender.WOMEN.value,
    'mens': Gender.MEN.value,
    'maternity': Gender.WOMEN.value,
    'toddler': Gender.KIDS.value,
    'toddlers': Gender.KIDS.value,
    'ballerinas': Gender.WOMEN.value,
    'ballerina': Gender.WOMEN.value,
    'aerie': Gender.WOMEN.value,
    'bra': Gender.WOMEN.value,
    'bridal': Gender.WOMEN.value,
    'necklace': Gender.WOMEN.value,
    'him': Gender.MEN.value,
    'women': Gender.WOMEN.value,
    'kids': Gender.KIDS.value,
    'girl': Gender.GIRLS.value,
    'boy': Gender.BOYS.value,
    'lingerie': Gender.WOMEN.value,
    'infant': Gender.KIDS.value,
    'infants': Gender.KIDS.value,
    'enfant': Gender.KIDS.value,
    'man': Gender.MEN.value,
    'newborn': Gender.KIDS.value,
    'forher': Gender.WOMEN.value,
    'child': Gender.KIDS.value,
    'children': Gender.KIDS.value,
    'childrens': Gender.KIDS.value,
    'childrenswear': Gender.KIDS.value,
    'plussize': Gender.WOMEN.value,
    'woman': Gender.WOMEN.value,
    'boys': Gender.BOYS.value,
    'girls': Gender.GIRLS.value,
    'ladies': Gender.WOMEN.value,
    'men': Gender.MEN.value,
    'babygirl': Gender.GIRLS.value,
    'babyboy': Gender.BOYS.value,
    'kidsgirls': Gender.GIRLS.value,
    'kidsboys': Gender.BOYS.value,
    'bride': Gender.WOMEN.value,
    'guys': Gender.BOYS.value,
    'junior': Gender.KIDS.value,
    'kid': Gender.KIDS.value,
    'baby': Gender.KIDS.value,
    'her': Gender.WOMEN.value,
    'teen': Gender.KIDS.value,
    'enfants': Gender.KIDS.value,
    'for her': Gender.WOMEN.value,
    'feminine': Gender.WOMEN.value,
    'gents': Gender.MEN.value,
    'unisex': Gender.ADULTS.value,
    'misses': Gender.WOMEN.value,
    'petites': Gender.WOMEN.value,
}


def map_gender(soup):
    soup = soup.lower()
    for gender_str, gender in GENDER_MAP.items():
        return gender if gender_str in soup else ''


def format_price(currency, current_price, previous_price=None):
    if previous_price and previous_price != current_price:
        previous_price = convert_price(previous_price)
        current_price = convert_price(current_price)

        if previous_price > current_price:
            return {
                'previous_price': previous_price,
                'current_price': current_price,
                'currency': currency
            }

        return {
            'previous_price': current_price,
            'current_price': previous_price,
            'currency': currency
        }

    return {
        'current_price': convert_price(current_price),
        'currency': currency
    }


def convert_price(price):
    return int(float(price) * 100)
