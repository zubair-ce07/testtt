import re
import scrapy
from scrape_woolworths.items import WoolWorthsItem
from scrapy.http import Request

DOWNLOAD_DELAY = 1


class WoolWorthsSpider(scrapy.Spider):
    name = 'woolworths_spider'
    allowed_domains = ['woolworths.co.za']
    start_urls = ['http://www.woolworths.co.za']

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse_main_nav)

    def parse_main_nav(self, response):
        main_nav_links = response.css('ul.nav-list--main li a::attr(href)').extract()[1:5]
        for link in main_nav_links:
            yield Request(self.start_urls[0] + link, callback=self.parse_categories)

    def parse_categories(self, response):
        all_categories = response.css('nav.horizontal-menu ul li a::attr(href)').extract()
        for category in all_categories:
            yield Request(self.start_urls[0] + category, callback=self.request_next_pages)

    def request_next_pages(self, response):
        pages = response.css('.pagination__page a::attr(href)').extract()
        for index in range(len(pages)):
            pages[index] = self.start_urls[0] + pages[index]
        pages.append(response.url)
        for page in pages:
            yield Request(page, callback=self.parse_listings, dont_filter=True)

    def parse_listings(self, response):
        product_list_items = response.css('div.product-list__item')
        product_urls = []
        for item in product_list_items:
            product_urls.append(item.css('a::attr(href)').extract_first())
        for product_url in product_urls:
            yield Request(self.start_urls[0] + str(product_url), callback=self.parse_woolworth_item)

    def parse_brand_name(self, response):
        return response.css('meta[itemprop="brand"]::attr(content)').extract_first()

    def parse_item_url(self, response):
        return response.url

    def parse_item_name(self, response):
        return response.css('input#gtmProductDisplayName::attr(value)').extract_first()

    def parse_description(self, response):
        description = response.css('meta[itemprop="description"]::attr(content)').extract()
        return self.clean_string(description)

    def parse_retailer_sku(self, response):
        return response.css('meta[itemprop="productId"]::attr(content)').extract_first()

    def parse_care_info(self, response):
        return response.css('div.accordion__content--chrome img::attr(src)').extract()

    def parse_category_info(self, response):
        return response.xpath('//input[contains(@id,"category")]/@value').extract_first()

    def parse_size_or_color_ids(self, ids_in_js, for_size):
        list_of_ids = []
        for id_js in ids_in_js:
            list_of_ids.append(re.findall('\((.*)\)', str(id_js))[0].split(',')[for_size])
        return list_of_ids

    def make_product_url(self, product_id, color_id, size_id):
        product_url = 'http://www.woolworths.co.za/store/fragments/product-common/ww/price.jsp?productItemId='\
                       + product_id + '&colourSKUId=' + color_id + '&sizeSKUId=' + size_id
        return product_url

    def parse_price_and_currency_info(self, response):
        currency = response.css('span[itemprop="priceCurrency"]::attr(content)').extract_first()
        price = response.css('span[itemprop="price"]::attr(content)').extract_first()
        woolworth_item = response.meta['woolworth_item']
        size = response.meta['size']
        color = response.meta['color']
        sku_id = '{}_{}'.format(color, size)
        woolworth_item['skus'][sku_id] = {'size': size, 'color': color, 'currency': currency, 'price': price}
        return self.request_another_sku_or_yield_item(woolworth_item, response.meta['skus_urls_and_info'])

    def request_another_sku_or_yield_item(self, woolworth_item, skus_urls_and_info):
        if skus_urls_and_info:
            sku_info = skus_urls_and_info.pop()
            url = sku_info[2]
            yield Request(url, callback=self.parse_price_and_currency_info, meta={
                'woolworth_item': woolworth_item, 'size': sku_info[1],
                'color': sku_info[0], 'skus_urls_and_info': skus_urls_and_info})
        else:
            yield woolworth_item

    def parse_sku_info(self, response, woolworth_item):
        product_size_color_ids_in_js = response.css('a.product-size::attr(onclick)').extract()
        size_ids = self.parse_size_or_color_ids(product_size_color_ids_in_js, 1)
        sizes = response.css('a.product-size::text').extract()
        color_ids_in_js = response.css('img.colour-swatch::attr(onclick)').extract()
        color_ids = self.parse_size_or_color_ids(color_ids_in_js, 0)
        colors = response.css('img.colour-swatch::attr(title)').extract()
        product_id = str(self.parse_retailer_sku(response))
        skus_urls_and_info = []
        for color_index in range(len(colors)):
            for size_index in range(len(sizes)):
                skus_urls_and_info.append([
                    colors[color_index],
                    sizes[size_index],
                    self.make_product_url(product_id, color_ids[color_index], size_ids[size_index])
                ])
        return self.request_another_sku_or_yield_item(woolworth_item, skus_urls_and_info)

    def check_if_string(self, variable):
        return isinstance(variable, str)

    def clean_string(self, attribute):
        if self.check_if_string(attribute):
            return re.sub('\s+', ' ', attribute)
        else:
            for index in range(len(attribute)):
                attribute[index] = re.sub('\s+', ' ', attribute[index])
            return attribute

    def parse_woolworth_item(self, response):
        woolworth_item = WoolWorthsItem()
        woolworth_item['brand'] = self.parse_brand_name(response)
        woolworth_item['url'] = self.parse_item_url(response)
        woolworth_item['name'] = self.parse_item_name(response)
        woolworth_item['description'] = self.parse_description(response)
        woolworth_item['retailer_sku'] = self.parse_retailer_sku(response)
        woolworth_item['care'] = self.parse_care_info(response)
        woolworth_item['category'] = self.parse_category_info(response)
        woolworth_item['skus'] = {}
        return self.parse_sku_info(response, woolworth_item)

