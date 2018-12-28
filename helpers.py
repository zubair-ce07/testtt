
def extract_price_details(price_record):
    price_details = {
        'old_price': float(price_record[0]) * 100,
        'price': float(price_record[1]) * 100,
    }
    return price_details
