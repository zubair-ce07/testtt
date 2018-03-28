from urllib.parse import urljoin
from w3lib.url import url_query_cleaner

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy import FormRequest, Request
from .base import BaseParseSpider, BaseCrawlSpider, clean
from skuscraper.parsers.currencyparser import CurrencyParser


class MixinAU:
    retailer = "lornajane-au"
    market = "AU"
    allowed_domains = ["lornajane.com.au"]
    start_urls = ["https://www.lornajane.com.au/"]


class MixinUS:
    retailer = "lornajane-us"
    market = "US"
    allowed_domains = ["lornajane.com"]
    deprecated = True
    start_urls = ["http://www.lornajane.com/"]


class LornaJaneParseSpider(BaseParseSpider):
    price_x = "//*[@class='main-product']//*[@class='price']//text()"
    size_xpath_t = '//*[contains(@id,"size_buttons") and contains(@id,"%s")]//input'
    unwanted_description = ['to see how to care for your new Lorna Jane.', 'Click', 'here']
    location_restriction = ['404 Page Not Found This page is not available in your region']

    def parse(self, response):
        product_id = self.product_id(response)

        garment = self.new_unique_garment(product_id)
        if not garment:
            return

        location_alert = clean(response.css('div.alert-danger'))
        if location_alert in self.location_restriction:
            return

        self.boilerplate_normal(garment, response)
        garment["image_urls"] = self.image_urls(response)
        garment["skus"] = self.skus(response)
        garment['meta'] = {'requests_queue': self.colour_requests(response)}
        return self.next_request_or_garment(garment)

    def product_id(self, response):
        return clean(response.css('[name=code]::attr(value)'))[0].split('_', 1)[0]

    def product_name(self, response):
        return clean(response.css('div.product-heading h1 ::text'))[0]

    def raw_description(self, response):
        return [x for x in clean(response.css('#desc2 ::text')) if x not in self.unwanted_description]

    def product_description(self, response):
        xpath = '//div[@itemprop="description"]/p[position()<3]//text()'
        description = clean(response.xpath(xpath))

        return description + [line for line in self.raw_description(response) if not self.care_criteria(line)]

    def product_care(self, response):
        return [line for line in self.raw_description(response) if self.care_criteria(line)]

    def product_brand(self, response):
        return "Lorna Jane"

    def product_category(self, response):
        return clean(response.css('.breadcrumb li>a::text'))[2:]

    def image_urls(self, response):
        return [urljoin(self.start_urls[0], x) for x in clean(response.css('.item img::attr(src)'))
                if 'missing_product' not in x]

    def skus(self, response):
        skus = {}
        currency = response.css('span[itemprop=priceCurrency]::attr(content)').extract()[0]
        colour = clean(response.css(".color-swatch a.selected ::attr(title)"))[0]
        sku_common = {'colour': colour, 'currency': CurrencyParser.currency(currency)}

        previous_price, sku_common['price'], _ = self.product_pricing(response)
        if previous_price:
            sku_common['previous_prices'] = previous_price

        for size in response.css(".second-div.size-charts a"):
            sku = sku_common.copy()
            sku['size'] = clean(size.css("::text"))[0]
            sku_id = clean(size.css('::attr(data-productcode)'))[0]
            skus[sku_id] = sku
            if size.css('[class*=disabled]'):
                sku["out_of_stock"] = True

        return skus

    def parse_colour(self, response):
        garment = response.meta['garment']
        garment['skus'].update(self.skus(response))
        garment['image_urls'].extend(self.image_urls(response))
        return self.next_request_or_garment(garment)

    def colour_requests(self, response):
        css = ".color-swatch a:not([class*=selected])::attr(data-url)"
        return [Request(response.urljoin(url), callback=self.parse_colour, dont_filter=True)
                for url in clean(response.css(css))]


class LornaJaneCrawlSpider(BaseCrawlSpider):
    listings_css = ['.pri-nav a[title~="Shop"]+div']
    products_css = ['div.product-item a.name']
    deny_r = ['/giftCard', '/lookbook', '/instashop', '/c-Activity', '/sisterhood', '/ActiveOutlet']

    rules = (
        Rule(LinkExtractor(restrict_css=listings_css, deny=deny_r), callback='parse_pagination'),
        Rule(LinkExtractor(restrict_css=products_css, deny=deny_r), callback='parse_item')
    )

    def parse_pagination(self, response):
        for req in self.parse_and_add_women(response):
            yield req

        response = response.replace(url=url_query_cleaner(response.url))
        css = "#loadMoreProductResultForm #page::attr(value)"
        current_page = response.css(css).extract_first(default="0")

        css = "#loadMoreProductResultForm #numberOfPages::attr(value)"
        total_page = response.css(css).extract_first(default="0")

        if int(current_page) > int(total_page):
            return

        yield FormRequest.from_response(response, formcss="#loadMoreProductResultForm",
                                        formdata={'partitial': 'false'}, callback=self.parse_pagination)


class AUParseSpider(MixinAU, LornaJaneParseSpider):
    name = MixinAU.retailer + '-parse'


class AUCrawlSpider(MixinAU, LornaJaneCrawlSpider):
    name = MixinAU.retailer + '-crawl'
    parse_spider = AUParseSpider()


class USParseSpider(MixinUS, LornaJaneParseSpider):
    name = MixinUS.retailer + '-parse'


class USCrawlSpider(MixinUS, LornaJaneCrawlSpider):
    name = MixinUS.retailer + '-crawl'
    parse_spider = USParseSpider()
