import asyncio
import time

import requests
import parsel


class Skus:
    def __init__(self, colour, price, currency, size, previous_prices,
                 sku_id, out_of_stock = None):

        self.colour = colour
        self.price = price
        self.currency = currency
        self.size = size
        self.previous_prices = previous_prices
        self.out_of_stock = out_of_stock
        self.sku_id = sku_id


class Sprinter:
    def __init__(self, retailer_sku, gender, category, brand, url, name,
                 description, care, image_urls, skus):
        self.retailer_sku = retailer_sku
        self.gender = gender
        self.category = category
        self.brand = brand
        self.url = url
        self.name = name
        self.description = description
        self.care = care
        self.image_urls = image_urls
        self.skus = skus


def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
            return i
    return -1


def get_description_and_care(selector):
    all_description_key = '//div[@class="features-delivery-inner"]//text()'
    all_description = selector.xpath(all_description_key).getall()
    description_titles_key = '//div[@class="features-delivery-inner"]' \
                             '//strong//text()'
    description_titles = selector.xpath(description_titles_key).getall()

    if not all_description:
        return "N/A", "N/A"

    all_description = [x.strip(' ').rstrip() for x in
                       all_description]
    all_description = list(filter(None, all_description))

    care_start_word = "Cómo cuidar"
    index = index_containing_substring(description_titles, care_start_word)

    if index == -1:
        description_titles_key = '//div[' \
                                 '@class="features-delivery-inner"]//b//text()'
        description_titles = selector.xpath(description_titles_key).getall()
        index = index_containing_substring(description_titles, care_start_word)
        if index == -1:
            return all_description, "N/A"

    if (index+1) >= len(description_titles):
        care_end_word = None
    else:
        care_end_word = description_titles[(index + 1)]

    description = list()
    care = list()
    care_string_start = False

    for word in all_description:
        if care_start_word in word:
            care_string_start = True

        if care_end_word == word:
            care_string_start = False

        if care_string_start:

            care.append(word)
        else:
            description.append(word)

    return description, care


def get_images_urls(selector):
    images_url_key = '//li[@class="product-thumb-item "]/img/@src'
    images_urls = selector.xpath(images_url_key).getall()
    images_urls = [urls.replace("84x84", "539x539") for urls in images_urls]
    return images_urls


def get_sku_id(selector):
    retailer_sku__key = '//span[@class="nmbrjga ' \
                        'js-product-code"]/text()'
    return selector.xpath(retailer_sku__key).get()


def get_gender(item_url, selector):
    url_details = item_url.split('/')
    gender = "N/A"
    gender_from_url = url_details[3].split('-')[-1]
    if gender_from_url == "nino" \
            or gender_from_url == "nina" \
            or gender_from_url == "hombre" \
            or gender_from_url == "mujer":
        gender = gender_from_url
    return gender


def get_categories(selector):
    bread_crumbs_key = '//span[@itemprop="name"]/text()'
    total_bread_crumbs = selector.xpath(bread_crumbs_key).getall()
    return list(total_bread_crumbs[1:-1])


def get_name(selector):
    name_key = '//h1[@class="product-main-title"]/text()'
    name = selector.xpath(name_key).get()
    name = ' '.join(name.split())
    return name


def get_sku(selector):
    colour_key = '//div[@class="ref-color"]//p/text()'
    colour = selector.xpath(colour_key).get()

    currency = "Euro"

    old_price_key = '//div[@class="price"]//p[' \
                    '@class="old-price"]//span//text()'

    new_price_key = '//div[@class="price"]//span//text()'

    old_prices = [selector.xpath(old_price_key).get()[:-2]]
    new_price = selector.xpath(new_price_key).get()[:-2]

    available_size_key = '//li[@class="nmbrjga available"]//text()'
    available_sizes = selector.xpath(available_size_key).getall()
    available_sizes = list(set(available_sizes))

    unavailable_size_key = '//li[@class="nmbrjga unavailable"]//text()'
    unavailable_sizes = selector.xpath(unavailable_size_key).getall()
    unavailable_sizes = list(set(unavailable_sizes))

    skus = list()
    for size in unavailable_sizes:
        sku_id = f"{colour}_{size}"
        sk = Skus(colour, new_price, currency, size, old_prices,
                         sku_id, True)
        skus.append(sk.__dict__)

    for size in available_sizes:
        sku_id = f"{colour}_{size}"
        sk = Skus(colour, new_price, currency, size, old_prices,
                         sku_id)
        skus.append(sk.__dict__)

    return skus


async def scrap_item_url(items_visited_urls, item_url, loop, sprinter_records):
    async with asyncio.BoundedSemaphore(5):
        future = loop.run_in_executor(None, requests.post, item_url)
        response = await future
        time.sleep(0.5)
        if response.status_code == 200 \
                and len(response.text):
            selector = parsel.Selector(text=response.text)

            retailer_sku = get_sku_id(selector)
            gender = get_gender(item_url, selector)
            categories = get_categories(selector)
            brand = "N/A"
            name = get_name(selector)
            description, care = get_description_and_care(selector)
            images_urls = get_images_urls(selector)
            skus = get_sku(selector)
            items_visited_urls[item_url] = True
            sp = Sprinter(retailer_sku, gender, categories, brand, item_url,
                          name, description, care, images_urls, skus)
            sprinter_records.append(sp)


async def schedule_items_futures(items_visited_urls, items_pending_urls,
                                 loop, sprinter_records):
    futures = []
    for item_url in items_pending_urls:
        futures.append(
            asyncio.ensure_future(scrap_item_url(items_visited_urls,
                                                 item_url, loop, sprinter_records)))
    await asyncio.wait(futures)
    return futures


def traverse_items(items_visited_urls, items_pending_urls, sprinter_records):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(schedule_items_futures(items_visited_urls,
                                                   items_pending_urls,
                                                   loop, sprinter_records))
