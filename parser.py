import asyncio
import time

import requests
import parsel

gender_map = [
    ('nino', 'boy'),
    ('nina', 'girl'),
    ('hombre', 'man'),
    ('mujer', 'woman')
]


def product_care(text_s):
    care_css = ".features-delivery-inner :contains('Cómo cuidar')+ul ::text"
    care = text_s.css(care_css).extract()
    care = [c.strip(' ').rstrip() for c in care]
    return list(filter(None, care))


def product_description(text_s):
    des_css = ".features-delivery-inner :contains('Características')+ul ::text"
    description = text_s.css(des_css).extract()
    description = [d.strip(' ').rstrip() for d in description]
    return list(filter(None, description))


def images_urls(text_s):
    image_url_css = ".product-thumb-item img::attr(src)"
    images = text_s.css(image_url_css).extract()
    return [urls.replace("84x84", "539x539") for urls in images]


def product_id(text_s):
    retailer_sku_css = '.js-product-code::text'
    return text_s.css(retailer_sku_css).extract_first()


def product_gender(item_url, text_s):
    gender = "unisex-adults"
    gender_css = '.product__category::text'
    gender_detail = text_s.css(gender_css).extract_first()
    soup = f'{item_url} {gender_detail}'.lower()
    for token, raw_gender in gender_map:
        if token in soup:
            gender = raw_gender
    return gender


def product_categories(text_s):
    product_category_css = '.custom-breadcrumb [itemprop="item"] span::text'
    return text_s.css(product_category_css).extract()


def product_name(text_s):
    name_css = '.product-main-title::text'
    name = text_s.css(name_css).extract_first()
    name = ' '.join(name.split())
    return name


def product_color(text_s):
    colour_css = '.ref-color :contains("Color: "):not(strong)::text'
    return text_s.css(colour_css).extract_first()


def prices(text_s):
    all_prices = dict()
    old_price_css = '.price .old-price span::text'
    new_price_css = '[itemprop="price"]::attr(content)'
    all_prices["currency"] = "Euro"
    all_prices["price"] = text_s.css(new_price_css).extract_first()
    all_prices["previous_prices"] = [text_s.css(old_price_css).extract_first()[:-2]]
    return all_prices


def all_sizes(text_s):
    sizes_css = '#mobile-size li::text'
    return text_s.css(sizes_css).extract()


def unavailable_sizes(text_s):
    unavailable_size_x = '#mobile-size .unavailable::text'
    return text_s.css(unavailable_size_x).extract()


def skus(text_s):
    skus = list()
    sizes = all_sizes(text_s)
    unavailable = unavailable_sizes(text_s)
    colour = product_color(text_s)
    common = prices(text_s)
    for size in sizes:
        sku = common.copy()
        sku["colour"] = colour
        if size in unavailable:
            sku["out_of_stock"] = True
        sku["sku_id"] = f"{colour}_{size}"
        skus.append(sku)
    return skus


async def parse(items_visited_urls, item_url, loop, sprinter_records):
    async with asyncio.BoundedSemaphore(5):
        future = loop.run_in_executor(None, requests.post, item_url)
        response = await future
        time.sleep(1)

        if response.status_code == 200 \
                and len(response.text):
            text_s = parsel.Selector(text=response.text)
            items_visited_urls.add(item_url)
            product_details = dict()
            product_details["retailer_sku"] = product_id(text_s)
            product_details["gender"] = product_gender(item_url, text_s)
            product_details["category"] = product_categories(text_s)
            product_details["brand"] = "sprinter"
            product_details["url"] = item_url
            product_details["name"] = product_name(text_s)
            product_details["description"] = product_description(text_s)
            product_details["care"] = product_care(text_s)
            product_details["image_urls"] = images_urls(text_s)
            product_details["skus"] = skus(text_s)
            sprinter_records.append(product_details)


async def schedule_items_futures(items_visited_urls, items_pending_urls,
                                 loop, sprinter_records):
    futures = []
    for item_url in items_pending_urls:
        futures.append(
            asyncio.ensure_future(parse(items_visited_urls, item_url, loop,
                                        sprinter_records)))
    await asyncio.wait(futures)
    return futures


def traverse_items(items_visited_urls, items_pending_urls, sprinter_records):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(schedule_items_futures(items_visited_urls,
                                                   items_pending_urls,
                                                   loop, sprinter_records))
