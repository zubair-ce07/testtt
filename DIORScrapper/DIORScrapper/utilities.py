"""
Helper module containing functions to parse item details
"""


def get_details(item_data):
    """
    parse and return details from item data
    :param item_data: JSON object containing product data
    :return: JSON object containing required data
    """
    return item_data['dataLayer']['ecommerce']['detail']['products']


def parse_category(item_data):
    """
    parse and return the category of the item
    :param item_data: JSON object containing product data
    :return: item category as string
    """
    if 'dataLayer' in item_data:
        if 'topCategory' in item_data['dataLayer']:
            return item_data['dataLayer']['topCategory']
    return None


def parse_name(item_data):
    """
    parse and return item name
    :param item_data: JSON object containing product data
    :return: item name as string
    """
    details = get_details(item_data)
    if 'name' in details:
        return details['name']
    return None


def parse_id(item_data):
    """
    parse and return item id
    :param item_data: JSON object containing product data
    :return: item id as string
    """
    details = get_details(item_data)
    if 'id' in details:
        return details['id']
    return None


def parse_price(item_data):
    """
    parse and return item price
    :param item_data: JSON object containing product data
    :return: item price as string
    """
    details = get_details(item_data)
    if 'price' in details:
        return details['price']
    return None


def parse_brand(item_data):
    """
    parse and return item brand name
    :param item_data: JSON object containing product data
    :return: item brand as string
    """
    details = get_details(item_data)
    if 'brand' in details:
        return details['brand']
    return None


def parse_variant(item_data):
    """
    parse and return item variant
    :param item_data: JSON object containing product data
    :return: item variant as string
    """
    details = get_details(item_data)
    if 'variant' in details:
        return details['variant']
    return None


def parse_status(item_data):
    """
    parse and return item status in inventory
    :param item_data: JSON object containing product data
    :return: item status
    """
    details = get_details(item_data)
    if details['dimension25']:
        return details['dimension25']
    return None


def parse_image_urls(item_data):
    """
    parse and return image urls
    :param item_data: JSON object containing product data
    :return: list of image urls
    """
    elements = item_data['cmsContent']['elements']
    image_urls = []
    for element in elements:
        if element:
            if element['type'] == "PRODUCTIMAGES":
                for image in element['images']:
                    if image['target'] == "DESKTOP":
                        image_urls.append(image['uri'])
    return image_urls


def parse_sizes(item_data):
    """
    parse and return sizes
    :param item_data: JSON object containing product data
    :return: list of item sizes
    """
    elements = item_data['cmsContent']['elements']
    sizes = []
    for element in elements:
        if element:
            if element['type'] == "PRODUCTVARIATIONS":
                if element['variationsType'] == "SIZE":
                    for size in element['variations']:
                        sizes.append(
                            {
                                'size': size['title'],
                                'status': size['status'],
                            }
                        )
    return sizes


def parse_colors(item_data):
    """
    parse and return colors
    :param item_data: JSON object containing product data
    :return: list of item colors
    """
    elements = item_data['cmsContent']['elements']
    colors = []
    for element in elements:
        if element:
            if element['type'] == "PRODUCTVARIATIONS":
                if element['variationsType'] == "SWATCH":
                    for color in element['variations']:
                        colors.append(color['title'])
    return colors


def parse_description(item_data):
    """
    parse and return item description
    :param item_data: JSON object containing product data
    :return: item description
    """
    description = None
    elements = item_data['cmsContent']['elements']
    for element in elements:
        if element:
            if element['type'] == "PRODUCTSECTIONDESCRIPTION":
                sections = element['sections']
                for section in sections:
                    if section['title'] == "THE DESCRIPTION":
                        description = section['content']
    return description


def parse_characteristics(item_data):
    """
    parse and return item characteristics
    :param item_data: JSON object containing product data
    :return: item characteristics
    """
    characteristics = None
    elements = item_data['cmsContent']['elements']
    for element in elements:
        if element:
            if element['type'] == "PRODUCTSECTIONDESCRIPTION":
                sections = element['sections']
                for section in sections:
                    if section['title'] == "THE CHARACTERISTICS":
                        characteristics = section['content']
    return characteristics
