from item import Product
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import scrapy
import urllib
import copy


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
        skus = {}
        params = {}

        brand = get_brand(response)
        care = get_care(response)
        detail_points = get_details(response)
        gender = 'Women'
        name = get_name(response)
        url = response.url
        image_urls = get_image_urls(response)
        sku = get_sku(response)
        version_id = get_version_id(response)
        anid = get_article_number(response)

        params["anid"] = anid
        params["cl"] ='oxwarticledetails'
        if version_id:
            params["varselid[0]"] = version_id.pop()

        url_color = create_url(params)

        request = scrapy.Request(url=url_color, callback=self.parse_color, dont_filter=True)

        product = Product(sku=sku, brand=brand, detail_points=detail_points, gender=gender, name=name, url=url,
                          image_urls=image_urls, skus=skus, care=care)

        request.meta['product'] = product
        request.meta['version_id'] = version_id
        request.meta['params'] = params

        yield request

    def parse_color(self, response):
        version_id = response.meta['version_id']
        product = response.meta['product']
        params = response.meta['params']

        product = create_color_skus(product,  response)

        if len(version_id) > 0:

            response.meta['version_id'] = version_id
            response.meta['product'] = product
            response.meta['params'] = params

            params["varselid[0]"] = version_id.pop()
            url_color = create_url(params)
            yield scrapy.Request(url_color, callback=self.parse_color, meta=response.meta, dont_filter=True)

        else:
            yield product


def create_url(params):
    url_params = urllib.urlencode(params)
    return 'https://www.sheego.de/index.php?' + url_params


def create_color_skus(product, response):
    skus = copy.deepcopy(product['skus'])
    sku = get_color_id(response)
    color = get_color(response)
    price = get_price(response)
    sizes = get_sizes(response)
    del sizes[0]
    for size in sizes:
        size = size.split("-")
        skus[sku + "_" + color + "_" + size[0]] = {"size": size[0], 'price': price, 'currency': 'euro', 'out_of_stock': size[1], 'color': color}

    product['skus'] = copy.deepcopy(skus)
    return product


def get_color_id(response):
    product_data = response.css('input.js-webtrends-data::attr(data-webtrends)').extract_first()
    product_data = product_data.split('","')
    sku = product_data[1]
    sku = sku.split('":"')
    return sku[1].strip('"')


def get_sizes(response):
    return clean(response.css('option::text').extract())


def get_color(response):
    return response.css('p.l-mb-5::text').extract()[1].strip()


def get_price(response):
    return response.css('input.js-lastprice::attr(value)').extract_first()


def get_version_id(response):
    return response.css('span.colorspots__item::attr(data-varselid)').extract()


def get_article_number(response):
    anid = response.css('span.js-artNr::text').extract_first()
    anid = anid.strip()
    return anid[:-2]


def get_sku(response):
    sku = response.css("meta[itemprop='sku']::attr(content)").extract_first()
    if not sku:
        product_data = response.css('input.js-webtrends-data::attr(data-webtrends)').extract_first()
        product_data = product_data.split('","')
        sku = product_data[1]
        sku = sku.split('":"')
        sku = sku[1].strip('"')
    return sku


def get_image_urls(response):
    return response.css("a[id='magic']::attr(href)").extract()


def get_name(response):
    return clean(response.css('h1.at-name::text').extract_first())


def get_details(response):
    return clean(response.css('ul.l-list').css('li::text').extract())


def get_care(response):
    return clean(response.css('div.l-mt-10').css('template.js-tooltip-content::text').extract())


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




