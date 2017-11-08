from scrapy.spiders import Rule
from scrapy.spiders import CrawlSpider
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

from FirstScrapyTask.items import HypedcItem


class HypeDcSpider(CrawlSpider):
    name = 'hypedc'
    start_urls = ['https://www.hypedc.com/']

    rules = (
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LxmlLinkExtractor(
            allow=['sneakers/', 'slides', 'casual', 'dress', 'boots', 'shoe-care', 'sandals', 'platforms', 'flats'
                , 'grade-school', 'youth', 'infant', 'baby'], deny=['pid'])),


        Rule(LxmlLinkExtractor(
            allow=['.html' ]), callback='parse_urls_of_products'),

        Rule(LxmlLinkExtractor(
            restrict_css='div.next.col-xs-4')),

    )

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    def parse_urls_of_products(self, response):

        product = HypedcItem()
        product['name'] = response.css('h1.product-name::text').extract_first()
        product['desc'] = response.css('div.product-description.std::text').extract_first().strip()

        category_info = response.css('ul.breadcrumb a::attr(title)').extract()
        product['category'] = ' / '
        product['category'] = product['category'].join(category_info[1:4])

        product['brand'] = response.css('h2.product-manufacturer::text').extract_first()
        product['color'] = response.css('h3.h4.product-colour::text').extract_first().strip()
        product['product_code'] = response.css('div.product-code::text').extract_first()

        product['url'] = response.url
        product['image_urls'] = response.css(
            'div.slider-inner.col-sm-13.col-sm-offset-11 img::attr(data-src)').extract()
        product['sizes_info'] = self.get_sizes(response)
        price_currency = self.get_price_currency(response)
        product['currency'] = price_currency[1]
        product['price_final'] = price_currency[0]

        yield product


    def get_price_currency(self ,response):
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

    def get_sizes(self ,response):
        size_categories = response.css('ul#size-selector-desktop-tabs li a::text').extract()
        stock_size = response.css('div#size-selector-tab-desktop-0 li::attr(data-stock)').extract()
        sizes = {}
        for index, size_type in enumerate(size_categories):
            size_type_values = '{0}{1}{2}'.format('div#size-selector-tab-desktop-', str(index), ' a::text')
            size_type_values = response.css(size_type_values).extract()
            sizes[size_type] = size_type_values

        sizes['Stock Status'] = stock_size
        return sizes