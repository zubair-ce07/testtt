
import urllib.parse
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from .base import BaseParseSpider, BaseCrawlSpider, clean


class Mixin:
    market = 'DE'
    retailer = 'sportscheck-de'
    lang = 'de'
    allowed_domains = ['www.sportscheck.com']
    start_urls_with_meta = [
        ('https://www.sportscheck.com/damen/', {'gender': 'women'}),
        ('https://www.sportscheck.com/herren/', {'gender': 'men'}),
        ('https://www.sportscheck.com/kinder/', {'gender': 'unisex-kids'}),
    ]


class SportScheckParseSpider(BaseParseSpider, Mixin):
    name = Mixin.retailer + '-parse'
    brands = ()
    price_css = '.price'

    BLACKLISTED_CATEGORIES = {'Ausrüstung', 'Sportarten', 'Fitnessgeräte'}
    # we only want Rucksäcke and Handschuhe which may fall under Ausrüstung or Sportarten
    WHITELISTED_CATEGORIES = {'Rucksäcke', 'Handschuhe'}

    GENDER_MAP = [
        ('damen', 'women'),
        ('herren', 'men'),
        ('mädchen', 'girls'),
        ('maedchen', 'girls'),
        ('jungen', 'boys'),
        ('kinder', 'unisex-kids'),
        ('junior', 'unisex-kids'),
    ]

    def parse(self, response):
        sku_id = self.product_id(response)
        garment = self.new_unique_garment(sku_id)
        if garment is None:
            return

        self.boilerplate_normal(garment, response)

        garment['gender'] = self.product_gender(response, garment)
        garment['skus'] = {}
        garment['image_urls'] = []
        garment['image_urls'] = self.image_urls(response)
        garment['meta'] = {'requests_queue': self.color_request(response)}

        return self.next_request_or_garment(garment)

    def parse_color(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        garment['image_urls'] += self.image_urls(response)

        return self.next_request_or_garment(garment)

    def create_url(self, url, id):
        params = {"ProductSKU": id}
        return url + '?' + urllib.parse.urlencode(params)

    def color_request(self, response):
        requests = []
        url = clean(response.css('form.small-12::attr(action)'))[0]
        color_sku_ids = clean(response.css('.colors__tile::attr(data-product-sku)'))
        for id in color_sku_ids:
            requests.append(Request(url=self.create_url(url, id), callback=self.parse_color))
        return requests

    def image_urls(self, response):
        url_end = "?$productimage_square$&w=400&aspect=1:1&qlt=70"
        url_start = "https://amp.sportscheck.com/i/sportscheck/"
        url_middle = clean(response.css('li::attr(data-amp-image-name)'))
        image_urls = []

        for mid in url_middle:
            image_urls.append(url_start+mid+url_end)

        return image_urls

    def skus(self, response):
        skus = {}
        color = clean(response.css('span.color-desc::text'))[0]
        common_sku = self.product_pricing_common_new(response)
        sizes = clean(response.css('#secondary-select option::attr(value)'))[1:]
        size_availability = clean(response.css('#secondary-select option::text'))[1:]
        itera = 0
        color_id = self.product_id(response)
        for size in sizes:
            sku = {}
            if 'Einheitsgröße' in size:
                sku['size'] = self.one_size
            else:
                sku['size'] = size

            if 'ausverkauft' in size_availability[itera]:
                sku['out_of_stock'] = True

            sku['color'] = color
            sku.update(common_sku)
            skus[color_id + "_" + size] = sku
            itera += 1

        return skus

    def product_id(self, response):
        return clean(response.css('input[name=ProductSKU]::attr(value)'))[0]

    def product_brand(self, response):
        xpath = '//div[@class="epdDescriptionManufacturer"]//@alt'
        brand = response.xpath(xpath).re('^Weitere Artikel von (.+)')
        if brand:
            return brand[0]
        brand = clean(response.xpath('//div[@itemprop="name"]/h1//span[@itemprop="brand"]/text()'))
        if brand:
            return brand[0]
        product_name = self.raw_name(response)
        for brand in self.brands:
            if product_name.lower().startswith(brand.lower() + " "):
                return brand

        return "SportScheck"

    def product_gender(self, response, garment):
        gender_part = [(response.xpath('//span[@id="headlineSecond"]/text()').extract() or [''])][0]
        to_match = ' '.join(gender_part).lower() + garment['url']
        for gender_str, gender in self.GENDER_MAP:
            if gender_str in to_match:
                return gender
        return garment['gender']

    def product_name(self, response):
        return clean(response.css('.product__desc::text'))[0]

    def product_description(self, response):
        return [x for x in self.raw_description(response) if not self.care_criteria(x)]

    def raw_description(self, response):
        description = []
        raw = clean(response.css('span.product-description__text ::text'))
        for x in raw:
            description += x.split(';')
        return description

    def product_care(self, response):
        return [x for x in self.raw_description(response) if self.care_criteria(x)]


def clean_url(value):
    pr = urllib.parse.urlparse(value)
    return pr.geturl().replace(';' + pr.params, '')


class SportScheckCrawlSpider(BaseCrawlSpider, Mixin):
    '''
    The only parts of the 'Ausrüstung' (Equipment) section that we would want to crawl are
    the following.

        Rucksaecke (backpacks)
        Handschuhe (gloves)

    We would only want to crawl relevant sections of the 'Sportarten' section,
        so the following types of items -

        clothing
        footwear
        accessories (Bags, hats, jewellery)
        Swimwear
        Socks

    Not these following types of items -

        Sports Equipment (rackets, balls, bicycles etc)
        Sports bandages
        Helmets
        Rollerblades

    However it does look like all clothing from this section is also listed under the relevant
    apparel sections of the site.
    '''
    download_delay = 0.25
    name = Mixin.retailer + '-crawl'
    parse_spider = SportScheckParseSpider()

    listings_css = [
        "div.small-2 a"
    ]

    deny_re = [
        r"/ausruestung/(?!rucksaecke|handschuhe)",
        "/sportarten/",
        # unwanted items tend to slip through new items or sale view all
        "/(neuheiten|sale)/(Damen|Herren|Kinder)/($|\d+/)",
        "/marken/",
        "/fitnessausruestung",
    ]

    products_css = ".productlist-item--overview__image"

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_re, process_value=clean_url), callback='parse'),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_item')
    )
