from item import Product
from scrapy.spiders import CrawlSpider
import scrapy
import urllib


class MotelSpider(CrawlSpider):
    name = 'Motelspider'
    domain = 'https://www.motelrocks.com/'

    def start_requests(self):
        urls = ['http://www.motelrocks.com/categories/CLOTHING/', 'http://www.motelrocks.com/categories/SWIMWEAR/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_pages)

    def parse_pages(self, response):
        links = response.css('div.xProductImage').css('a::attr(href)').extract()
        params = {"invocation": "page", "page": str(response.css('div.pageitem::attr(pagenum)')[-1].extract())}
        next_page = create_url(params)

        if str(response.css('div.pageitem::text')[-1].extract()) == 'Next':
            yield scrapy.Request(next_page, callback=self.parse_pages, meta=response.meta, dont_filter=True)

        for link in links:
            yield scrapy.Request(link, callback=self.parse)

    def parse(self, response):

        gender = "women"
        name_color = get_name_color(response)
        name = name_color[0]
        brand = "Motel"
        color = name_color[1]
        url = response.url
        image_urls = get_image_urls(response)
        details = get_details(response)
        sku = get_sku(response)
        skus = build_skus(response, sku, color)

        product = Product(sku=sku, name=name, brand=brand, gender=gender, url=url, image_urls=image_urls, skus=skus,
                          details=details)

        return product


def create_url(params):
    url_params = urllib.urlencode(params)
    return 'http://www.motelrocks.com/categories/CLOTHING?' + url_params


def build_skus(response, sku, color):
    price = get_price(response)
    sizes = get_sizes(response)
    availability = get_availability(response)

    skus = {}
    itera = 0
    for size in sizes:
        skus[sku+"_"+color+"_"+size] = {"price": price, "color": color, "size": size, "availability": availability[itera]}
        itera += 1

    return skus


def get_availability(response):
    return map(bool, map(int, response.css('li.sizeli::attr(instock)').extract()))


def get_sizes(response):
    return clean_list(response.css('li.sizeli::text').extract())


def get_price(response):
    return response.css('div.xProductPriceRating').css('strong::text').extract_first()


def get_sku(response):
    return response.css('input[name="product_id"]::attr(value)').extract_first()


def get_details(response):
    return ''.join(response.css('div[id=Details]').css('span::text').extract())


def get_image_urls(response):
    return response.css('li.prodpicsidethumb').css('img::attr(src)').extract()


def get_name_color(response):
    return split_name_brand(response.css('h1[itemprop=name]::text').extract_first())


def split_name_brand(name):
    if 'in' in name:
        name = name.split(' in ')
    if 'by' in name[1]:
        color = name[1].split(' by ')
        return [name[0], color[0]]

    return name


def clean_list(lists):
    itera = 0
    for l in lists:
        lists[itera] = l.strip()
        itera += 1

    lists = filter(None, lists)
    return lists
