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


def cleaner(product_record):
    return list(filter(None, [p.strip(' ').rstrip() for p in product_record]))


def product_care(text_s):
    care_css = ".features-delivery-inner :contains('Cómo cuidar')+ul ::text"
    care = text_s.css(care_css).extract()
    return cleaner(care)


def product_description(text_s):
    des_css = ".features-delivery-inner :contains('Características')+ul ::text"
    description = text_s.css(des_css).extract()
    return cleaner(description)


def images_urls(text_s):
    image_url_css = ".product-thumb-item img::attr(src)"
    images = text_s.css(image_url_css).extract()
    return [urls.replace("84x84", "539x539") for urls in images]


def product_id(text_s):
    return text_s.css('.js-product-code::text').extract_first()


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
    name = text_s.css('.product-main-title::text').extract_first()
    name = ' '.join(name.split())
    return name


def product_color(text_s):
    colour_css = '.ref-color :contains("Color: "):not(strong)::text'
    return text_s.css(colour_css).extract_first()


def product_pricing(text_s):
    prices = dict()
    prices["currency"] = "Euro"
    price_css = '[itemprop="price"]::attr(content)'
    prices["price"] = text_s.css(price_css).extract_first()
    prices["previous_product_pricing"] = [
        text_s.css('.price .old-price span::text').extract_first()[:-2]]
    return prices


def skus(text_s):
    skus = list()
    sizes = text_s.css('#mobile-size li::text').extract()
    unavailable = text_s.css('#mobile-size .unavailable::text').extract()
    colour = product_color(text_s)
    common = product_pricing(text_s)
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


async def schedule_items_futures(items_visited_urls, items_urls,
                                 loop, sprinter_records):
    futures = []
    for url in items_urls:
        futures.append(asyncio.ensure_future(parse(items_visited_urls,
                                                   url, loop,
                                                   sprinter_records)))
    await asyncio.wait(futures)
    return futures


def traverse_items(items_visited_urls, items_urls, sprinter_records):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(schedule_items_futures(items_visited_urls,
                                                   items_urls,
                                                   loop, sprinter_records))
