def extract_price_details(price_record):
    price_details = {
        'old_price': float(price_record[0]) * 100 if price_record[0] else None,
        'price': float(price_record[1]) * 100 if price_record[1] else None,
    }
    return price_details

