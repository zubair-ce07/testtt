from item import Product
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SheegoSpider(CrawlSpider):
    name = 'SheegoSpider'
    domain = 'https://www.sheego.de'

    start_urls = [
        'https://www.sheego.de/mode/damenmode/',
        'https://www.sheego.de/damenmode/accessoires-schmuck/',
        'https://www.sheego.de/damenwaesche/',
        'https://www.sheego.de/waesche-bademode/night-homewear/',
        'https://www.sheego.de/damen-bademode/',
        'https://www.sheego.de/schuhe/schuhtypen/',
    ]

    rules = (
        Rule(LinkExtractor(restrict_css='span.paging__btn')),
        Rule(LinkExtractor(restrict_css='a.product__top'), callback='parse_product'),
    )

    def parse_product(self, response):
        brand = get_brand(response)
        care = get_care(response)
        detail_points = get_details(response)
        gender = 'Women'
        name = get_name(response)
        url = response.url
        image_urls = get_brand(response)
        sku = get_sku(response)
        color = get_color(response)
        sizes = get_sizes(response)
        price = get_price(response)
        skus = create_skus(color, sizes, sku, price)

        product = Product(sku=sku, brand=brand, detail_points=detail_points, gender=gender, name=name, url=url,
                                   image_urls=image_urls, skus=skus, care=care)
        return product


def get_price(response):
    return response.css('meta[itemprop="price"]::attr(content)').extract()


def get_sizes(response):
    sizes = response.css("select.form-group--select").css('option::text').extract()
    if sizes:
        del sizes[0]
    return sizes


def get_color(response):
    return response.css('span.colorspots__item::attr(title)').extract()


def get_sku(response):
    sku = response.css("meta[itemprop='sku']::attr(content)").extract_first()
    if not sku:
        product_data = response.css('input.js-webtrends-data::attr(data-webtrends)').extract_first()
        product_data = product_data.split(',')
        sku = product_data[1]
        sku = sku.split(':')
        return sku[1].strip('"')


def get_image_urls(response):
    return response.css("a[id='magic']::attr(href)").extract()


def get_name(response):
    name = response.css('h1.at-name::text').extract_first()
    return clean(name)


def get_details(response):
    detail_points = response.css('ul.l-list').css('li::text').extract()
    return clean(detail_points)


def get_care(response):
    care = response.css('div.l-mt-10').css('template.js-tooltip-content::text').extract()
    return clean(care)


def get_brand(response):
    brand = response.css('section.p-details__brand').css('a::text').extract_first()
    if not brand:
        brand = response.css('section.p-details__brand::text').extract_first()
    return clean(brand)


def clean(x):
    if type(x) == unicode:
        x = x.strip()
    else:
        itera = 0
        for c in x:
            x[itera] = c.strip()
            itera += 1
    return x


def create_skus(color, sizes, sku, price):
    skus = {}
    for c in color:
        if sizes:
            for size in sizes:
                details = {}
                size = size.strip()
                size = size.split("-")
                details['color'] = c
                details['size'] = size[0]
                details['availability'] = size[1]
                details['price'] = price
                skus[sku+"_"+c+"_"+size[0]] = details
            del details
        else:
            details = {}
            details['color'] = c
            details['price'] = price
            skus[sku + "_" + c] = details
            del details

    return skus