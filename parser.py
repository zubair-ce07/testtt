import asyncio
import time

import requests
import parsel

gender_translator = [
    ('nino', 'boy'),
    ('nina', 'girl'),
    ('hombre', 'man'),
    ('mujer', 'woman')
]


class Sprinter:
    def __init__(self, retailer_sku, gender, category, brand, url, name,
                 description, care, image_urls, product_skus):
        self.sprinter_records = dict()
        self.sprinter_records["retailer_sku"] = retailer_sku
        self.sprinter_records["gender"] = gender
        self.sprinter_records["category"] = category
        self.sprinter_records["brand"] = brand
        self.sprinter_records["url"] = url
        self.sprinter_records["name"] = name
        self.sprinter_records["description"] = description
        self.sprinter_records["care"] = care
        self.sprinter_records["image_urls"] = image_urls
        self.sprinter_records["skus"] = product_skus


def product_care(selector):
    care_css = ".features-delivery-inner :contains('Cómo cuidar')+ul ::text"
    care = selector.css(care_css).extract()
    care = [c.strip(' ').rstrip() for c in care]
    return list(filter(None, care))


def product_description(selector):
    des_css = ".features-delivery-inner :contains('Características')+ul ::text"
    description = selector.css(des_css).extract()
    description = [d.strip(' ').rstrip() for d in description]
    return list(filter(None, description))


def images_urls(selector):
    image_url_css = ".product-thumb-item>img::attr(src)"
    images = selector.css(image_url_css).extract()
    return [urls.replace("84x84", "539x539") for urls in images]


def product_id(selector):
    retailer_sku_css = '.js-product-code::text'
    return selector.css(retailer_sku_css).extract_first()


def product_gender(item_url, selector):
    url_details = item_url.split('/')
    gender = "unisex"
    gender_from_url = url_details[3].split('-')[-1]
    gender_css = '.product__category::text'
    gender_detail = selector.css(gender_css).extract_first()
    global gender_translator
    for spanish, english in gender_translator:
        if gender_from_url == spanish:
            gender = english
        elif spanish in gender_detail:
            gender = english
    return gender


def product_categories(selector):
    product_category_css = 'span[itemprop="name"]::text'
    product_category = selector.css(product_category_css).extract()
    return list(product_category[1:-1])


def product_name(selector):
    name_css = '.product-main-title::text'
    name = selector.css(name_css).extract_first()
    name = ' '.join(name.split())
    return name


def product_color(selector):
    colour_css = '.ref-color>p::text'
    return selector.css(colour_css).extract_first()


def prices(selector):
    all_prices = dict()
    old_price_css = '.price>p.old-price>span::text'
    new_price_css = '.price>p>span::text'
    all_prices["currency"] = "Euro"
    all_prices["price"] = selector.css(new_price_css).extract_first()[:-2]
    all_prices["previous_prices"] = [selector.css(old_price_css).extract_first(
    )[:-2]]
    return all_prices


def all_sizes(selector):
    sizes_css = '#mobile-size>li::text'
    return selector.css(sizes_css).extract()


def unavailable_sizes(selector):
    unavailable_size_x = '#mobile-size>.unavailable::text'
    return selector.css(unavailable_size_x).extract()


def skus(selector):
    skus = list()
    sizes = all_sizes(selector)
    unavailable = unavailable_sizes(selector)
    colour = product_color(selector)
    common = prices(selector)
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
            selector = parsel.Selector(text=response.text)

            retailer_sku = product_id(selector)
            gender = product_gender(item_url, selector)
            categories = product_categories(selector)
            brand = "N/A"
            name = product_name(selector)
            description = product_description(selector)
            care = product_care(selector)
            images = images_urls(selector)
            product_skus = skus(selector)
            items_visited_urls[item_url] = True
            spr = Sprinter(retailer_sku, gender, categories, brand, item_url,
                           name, description, care, images, product_skus)
            sprinter_records.append(spr.sprinter_records)


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
