from .mappings import Mapping

def get_price(current_price):
    current_price = [(float(x.replace(u',', u'.')))*100 for x in current_price]
    return current_price 


def gender_extractor(data):
    for gender in Mapping.gender_map.keys():
        if gender in data:
            return gender
