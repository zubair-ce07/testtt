import scrapy
from crawler_kith.items import CrawlerKithItem
import json


class CrawlerKith(scrapy.Spider):
    name = "kith"
    items = []
    categories = ['Footwear', 'Apparel', 'Accessories', 'Sale']

    def start_requests(self):
        start_url = [
            'https://kith.com/',
        ]
        for url in start_url:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for customer_href in response.css(
                'li.ksplash-header-upper-item a::attr(href)'
        ).extract():
            if 'kithland' not in customer_href:
                if not customer_href == '/':
                    yield response.follow(customer_href, self.parse)
                if 'kid' in customer_href:
                    category_href = response.xpath(
                        '//li[@class="main-nav-list-item"]/a[starts-with(text(), "Shop")]/@href'
                    ).extract_first()
                    yield response.follow(category_href, self.parse_all_products)
                else:
                    for category in self.categories:
                        category_href = response.xpath(
                            '//li[@class="main-nav-list-item"]/a[starts-with(text(), "' + category + '")]/@href'
                        ).extract_first()
                        yield response.follow(category_href, self.parse_all_products)

    def parse_all_products(self, response):
        all_hrefs = response.xpath(
            '//a[@class="product-card-info"]/@href'
        ).extract()
        for href in all_hrefs:
            yield response.follow(href, self.parse_one_item)
        next_page = response.xpath(
            '//span[@class="next"]/a/@href'
        ).extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse_all_products)

    def parse_one_item(self, response):
        items = []
        item = CrawlerKithItem()
        item["name"] = response.xpath(
            '//meta[@property="og:title"]/@content'
        ).extract_first()
        item["brand"] = get_brand(response)
        item['category'] = get_brand(response)
        item["care"] = get_description(response)[-1]
        item["description"] = ",".join(get_description(response)[:-1])
        item["gender"] = get_gender(response.url)
        item['image_urls'] = get_all_images(response)
        item['market'] = get_market(response)
        item['retailer'] = get_retailer(response)
        item['retailer_sku'] = response.xpath(
            '//input[@id="product_id"]/@value'
        ).extract_first()
        item['published_at'] = get_item_from_html(response, 'published_at')
        item['created_at'] = get_item_from_html(response, 'created_at')
        item['skus'] = get_skus(response)
        item['url'] = get_url(response)
        item['url_original'] = response.url

        items.append(item)
        return items


def get_all_images(response):
    return response.xpath(
        '//div[@class="super-slider-thumbnails-slide-wrapper"]/img/@src'
    ).extract()


def get_description(response):
    description = response.xpath(
        '//meta[@property="og:description"]/@content'
    ).extract_first().split('\n')
    return list(filter(('').__ne__, description))


def get_url(response):
    return response.xpath(
        '//meta[@property="og:url"]/@content'
    ).extract_first()


def get_retailer(response):
    name = response.xpath(
        '//meta[@property="og:site_name"]/@content'
    ).extract_first()
    return name + '-' + get_market(response)


def get_brand(response):
    brand_tag = response.xpath(
        '//script[@text="text/javascript"]'
    ).extract_first().split(';')
    for word in brand_tag:
        if 'var item =' in word:
            word = word.replace('var item = ', '').replace('\n', '')
            for literal in word.split(","):
                if 'Brand' in literal:
                    literal = literal.split('"')
                    return literal[1]


def get_item_from_html(response, to_find):
    script_tag = response.xpath(
        '//script[text()[contains(., "(function($){")]]'
    ).extract_first()
    script_tag = script_tag.split(';')
    for word in script_tag:
        if 'var product =' in word:
            word = word.replace('var product = ', '').replace('\n', '')
            data = json.loads(word)
            try:
                return data[to_find]
            except KeyError:
                return None


def get_market(response):
    if get_currency(response) == 'USD':
        return 'US'
    return '-'


def get_currency(response):
    return response.xpath(
        '//meta[@itemprop="priceCurrency"]/@content'
    ).extract_first()


def get_skus(response):
    all_variants = get_item_from_html(response, 'variants')
    skus = {}
    for variant in all_variants:
        empty = dict()
        empty['colour'] = variant['name'].split('-')[1][1:-1]
        empty['currency'] = get_currency(response)
        empty['price'] = variant['price']
        empty['size'] = variant['title']
        empty['ID'] = variant['id']
        sku = variant['sku']
        skus[sku] = empty
    return skus


def get_gender(href):
    href = href.lower()
    if 'kids' in href:
        return 'Kids'
    elif 'women' in href:
        return 'Women'
    else:
        return 'Men'
