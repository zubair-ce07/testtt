from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from OspraySpider.items import MotelSpiderItem
from scrapy import Request
from scrapy import FormRequest


class MotelRocksSpider(CrawlSpider):
    name = "motel"
    allowed_domains = ["motelrocks.com"]
    start_urls = ['http://www.motelrocks.com/',
                 ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('ul.dropdown > li > a',)), callback="parse_pages"),
    )

    def parse_pages(self, response):
        category_id = response.css('link[type="application/rss+xml"]::attr(href)').re('categoryid=([\d]+)')[0]
        pg_size = response.css('#fnps::attr(value)').extract_first()
        for page_num in range(1, int(response.css('#sc6>div::text').extract()[-2]) + 1):
            form_data = {
                'isajax': '1',
                'categoryid': category_id,
                'catid': category_id,
                'sortby': 'etailpreferred',
                'invocation': 'page',
                'page': str(page_num),
                'pagesize': pg_size
            }
            yield FormRequest("http://www.motelrocks.com/categories_ajax.php", formdata=form_data, callback=self.parse_products)

    def parse_products(self, response):
        for url in response.css('div.catproddiv > div.xProductImage > a:first_child::attr(href)').extract():
            yield Request(url, callback=self.parse_items)

    def parse_items(self, response):
        item = MotelSpiderItem()
        item.setdefault('gender', 'female')
        item.setdefault('brand', 'Motel')
        item['category'] = self.get_category(response)
        item['care'] = self.get_care(response)
        item['description'] = self.get_description(response)
        item['image_urls'] = [self.get_image(response)]
        item['name'] = [self.get_product_name(response)]
        item['skus'] = self.get_skus(response)
        item['url'] = response.url
        item['url_original'] = response.url
        item['retailer_sku'] = self.get_sku_id(response)
        yield item

    def get_skus(self, response):
        sku_id = self.get_sku_id(response)
        sizes = self.get_sizes(response)
        price = self.get_price(response)
        currency_codes = {'$': 'DOL', '€': 'EUR', '£': 'POU'}
        currency = None
        price_literals = ""
        result = {}
        for letter in price:
            if letter.isdigit():
                price_literals += letter
            else:
                currency = currency_codes[letter]
        color = self.get_current_color(response)
        for size in sizes:
            stock_info = {}
            formatted_size = size.strip('Unavailable-')
            if 'Unavailable' in size:
                stock_info.update({'out_of_stock': True})
            sku_size_identifier = '{0}_{1}'.format(sku_id, formatted_size)
            result[sku_size_identifier] = {
                'colour': color,
                'currency': currency,
                'price': int(price_literals),
                'size': formatted_size
            }
            result[sku_size_identifier].update(stock_info)
        return result

    def get_care(self, response):
        return response.css('#Details>p:nth_child(3)>span ::text').extract()

    def get_description(self, response):
        return response.css('#Details>p:nth_child(2)>span ::text').extract()

    def get_sku_id(self, response):
        return response.css('input[name="product_id"]::attr(value)').extract_first()

    def get_image(self, response):
        return response.css("#main-image::attr(src)").extract_first()

    def get_current_color(self, response):
        return response.css('#colourswatch>a[href="'+response.url+'"]::attr(title)').extract_first()

    def get_product_name(self, response):
        return response.css('#product-desc>h1::text').extract_first()

    def get_price(self, response):
        prices = response.css("em[itemprop='price']")
        return prices.css('::text').extract_first() if prices.css('::text') else \
            prices.css('span::text').extract_first()

    def get_sizes(self, response):
        sizes = []
        for size in response.css('div.ProductOptionList div.left > ul> li'):
            size_keyword = ""
            if size.css('[stockqty="0"]'):
                size_keyword += "Unavailable-"
            text = list(filter(None, [i.strip() for i in size.css('::text').extract()]))[0]
            sizes.append('{0}{1}'.format(size_keyword, text))
        return sizes

    def get_category(self, response):
        return response.css('ul.breadcrumbs>li span::text').extract()
