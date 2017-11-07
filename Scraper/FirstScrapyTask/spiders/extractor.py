import scrapy
from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors import LinkExtractor

from FirstScrapyTask.items import ProductInfo


def get_sizes(response):
    size_categories = response.css('ul#size-selector-desktop-tabs li a::text').extract()
    stock_size = response.css('div#size-selector-tab-desktop-0 li::attr(data-stock)').extract()
    sizes = {}
    for index, size_type in enumerate(size_categories):
        size_type_values = '{0}{1}{2}'.format('div#size-selector-tab-desktop-', str(index), ' a::text')
        size_type_values = response.css(size_type_values).extract()
        sizes[size_type] = size_type_values

    sizes['Stock Status'] = stock_size
    return sizes


def get_price_currency(response):
    price_in_dollars = str(response.css('span.price-dollars::text').extract_first())
    price_in_cents = str(response.css('span.price-cents::text').extract_first())

    # For Discounted Sale Price
    if not price_in_dollars:
        price = str(response.css('p.special-price span.price::text').extract_first())
        price = price.strip()
        currency = price[0:1]
        return [price, currency]

    # For Original Sale Price
    else:
        currency = price_in_dollars[0:1]
        price = price_in_dollars + price_in_cents
        return [price, currency]


class HypeDcSpider(CrawlSpider):
    name = 'hypedc'
    start_urls = ['https://www.hypedc.com/']

    rules = (
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(
            allow=['sneakers/', 'slides', 'casual', 'dress', 'boots', 'shoe-care', 'sandals', 'platforms', 'flats'
                , 'grade-school', 'youth', 'infant', 'baby'], deny=['pid']), callback='parse_urls_of_products'),
    )

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def parse_urls_of_products(self, response):
        all_urls = response.css('div.item a::attr(href)').extract()

        # calling scrapy request for all the urls extracted from main page
        for url in all_urls:
            request = scrapy.Request(url=url, callback=self.parse_results_from_urls)
            yield request

        next_page = response.css('div.category-page-products div.next.col-xs-4 a::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse_urls_of_products)

    def parse_results_from_urls(self, response):

        product_info = ProductInfo()
        product_info['name'] = response.css('h1.product-name::text').extract_first()
        product_info['desc'] = response.css('div.product-description.std::text').extract_first()
        product_info['desc'] = product_info['desc'].strip()

        category_info = response.css('ul.breadcrumb a::attr(title)').extract()

        product_info['category'] = '{} / {} / {}'.format(category_info[1] , category_info[2] , category_info[3])

        product_info['brand']= response.css('h2.product-manufacturer::text').extract_first()
        product_info['color'] = response.css('h3.h4.product-colour::text').extract_first()
        product_info['color'] = product_info['color'].strip()
        product_info['product_code'] = response.css('div.product-code::text').extract_first()

        product_info['url'] = response.url
        product_info['image_urls'] = response.css('div.slider-inner.col-sm-13.col-sm-offset-11 img::attr(data-src)').extract()
        product_info['sizes_info'] = get_sizes(response)
        price_currency = get_price_currency(response)
        product_info['currency'] = price_currency[1]
        product_info['price_final'] = price_currency[0]

        yield product_info
