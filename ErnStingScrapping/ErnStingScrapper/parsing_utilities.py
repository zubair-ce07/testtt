"""
Helper module to contain all the parsing logic of a product
"""

def get_category_id(response):
    """
    parse the category id from given item response
    :param response: response object to parse
    :return: category id to be used in yielding Request
    """
    scripts_path = "script[type *= 'text/javascript']::text"
    scripts = response.css(scripts_path).extract()
    return scripts[3].split('categoryId = "')[1].split('"')[0]


def get_product_count(response):
    """
    parse and return the total items of a category
    :param response: response object to parse
    :return: total no of items
    """
    product_count_path = ".product-count-holder::text"
    return response.css(product_count_path).extract_first()


def format_page_urls(response, page_no):
    """
    create and return the final page url to be fetched
    :param response: response object to parse
    :param page_no: page no to add in url
    :return: page url to fetch items from
    """
    full_url = (
        'https://www.ernstings-family.de:443/wcs/'
        'resources/store/10151/productview/bySearchTermDetails/'
        '*?pageNumber={}&pageSize=24&categoryId={}'
    )
    category_id = get_category_id(response)
    return full_url.format(page_no, int(category_id))


def get_page_urls(response):
    """
    create and return a list of all pages of a category
    :param response: response object to parse
    :return: list of page urls to fetch
    """
    page_urls = []
    total_items = get_product_count(response)
    if total_items:
        # get total item count for sub-category
        total_item_count = int(total_items.split(" ")[0])
        # find max pages to crawl
        max_page = int(total_item_count / 24) + 1
        # generate urls of pages
        for curr_page in range(1, max_page + 1):
            page_urls.append(format_page_urls(response, curr_page))
    # return page urls to crawl
    return page_urls


def parse_image_paths(item):
    """
    parse and return image urls of given item
    :param item: item to parse
    :return: list of image urls
    """
    base_image_path = "//images.ernstings-family.com/product_detail/"
    images = []
    for val in range(len(item['Attachments'])):
        image_name = item['Attachments'][val]['path']
        images.append(base_image_path + image_name)
    return images


def parse_labels(item):
    """
    parse and return item labels
    :param item: item to parse
    :return: list of labels
    """
    labels = []
    if item['xcatentry_issale'] == '1':
        labels.append("sale")
    if item['xcatentry_isnew'] == '1':
        labels.append("neu")
    return labels


def parse_item_skus(item):
    """
    parse and return item skus
    :param item: item to parse
    :return: list of skus
    """
    sku_count = item['numberOfSKUs']
    skus = []
    for var in range(int(sku_count)):
        current_sku = item['SKUs'][var]
        sku_id = current_sku['SKUUniqueID']
        sku_size = current_sku['Attributes'][0]['Values'][0]['values']
        sku_price = current_sku['Price'][0]['SKUPriceValue']
        skus.append({'id': sku_id,
                     'size': sku_size,
                     'price': sku_price})
    return skus


def parse_item_detail(item):
    """
    parse and return detail of an item
    :param item: item to parse
    :return: detail of item
    """
    detail = ""
    attributes = item['Attributes']
    for attribute in attributes:
        if attribute['identifier'] == 'details':
            description = attribute['Values'][0]['values']
            detail = description.split("</p>")[0].split("<p>")[1]
            detail += "\n"
            points_string = description.split("</ul>")[0]
            points_string = points_string.split("<p>")[1]
            points_string = points_string.split("</p>")[1]
            points = points_string.split("<li>")
            for point in points[1:]:
                detail += point.replace("</li>\n", "")
    return detail


def parse_item_material(item):
    """
    parse and return material of item
    :param item: item to parse
    :return: material description of item
    """
    material = ""
    attributes = item['Attributes']
    for attribute in attributes:
        if attribute['identifier'] == 'material':
            description = attribute['Values'][0]['values']
            materials = description.split("</ul>")[0].split("<li>")
            for mat in materials[1:]:
                material += mat.replace("</li>\n", "")
    return material


def parse_item_colors(item):
    """
    parse and return the list of item colors
    :param item: item to parse
    :return: list of item colors
    """
    colors = []
    attributes = item['Attributes']
    for attribute in attributes:
        if attribute['identifier'] == 'search_color':
            color_list = attribute['Values']
            for val in range(len(color_list)):
                color = color_list[val]['values']
                colors.append(color)
    return colors


def parse_item_name(item):
    """
    parse and return item name
    :param item: item to parse
    :return: item name
    """
    return item['name']


def parse_item_url(item):
    """
    parse and return item resource id
    :param item: item to parse
    :return: item resource id url
    """
    return item['resourceId']

