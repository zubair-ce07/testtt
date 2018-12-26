import json


def extract_price_details(price_record, size_record):
    price_details = {
        'price': float(price_record[0]) * 100 if price_record else None,
        'old_price': float(json.loads(size_record[0])['amount']) * 100 if size_record else None,
        'currency': price_record[1] if price_record else None,
    }
    return price_details
