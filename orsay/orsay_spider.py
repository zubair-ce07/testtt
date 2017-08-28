import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrape_orsay.items import OrsayItem


class OrsaySpider(CrawlSpider):
    name = "orsay_spider"
    allowed_domains = ["orsay.com"]
    start_urls = ['http://www.orsay.com/']

    rules = (
        Rule(LinkExtractor(restrict_css=('div#topMenu-container a', 'div.pages li.arrow a',))),
        Rule(LinkExtractor(restrict_css=('div.product-shop a',)), callback='parse_orsay_item'),
    )

    def parse_brand_name(self):
        return 'Orsay'

    def parse_category_info(self, response):
        return response.css('div.product-view input[name="category_name"]::attr(value)').extract_first()

    def parse_description_info(self, response):
        return [response.css('div.product-info-and-care p.description::text').extract_first().strip()]

    def parse_item_name(self, response):
        return response.css('div.product-essential .product-name::text').extract_first()

    def parse_item_url(self, response):
        return response.url

    def parse_retailer_sku_info(self, response):
        return response.css('div#contact-modal input#sku::attr(value)').extract_first()[:-2]

    def parse_gender(self):
        return 'women'

    def parse_item_other_color_urls(self, response):
        return response.css('ul.product-colors li a::attr(href)').extract()[1:]

    def parse_care_info(self, response):
        material = response.css('div.product-care p.material::text').extract_first()
        care_images = response.css('div.product-care ul.caresymbols img::attr(src)').extract()
        return [material] + care_images

    def parse_image_urls(self, response):
        return response.css('div.product-image-gallery a::attr(href)').extract_first()

    def parse_sku_color_info(self, response, orsay_item):
        orsay_item['image_urls'].append(self.parse_image_urls(response))
        product_id = response.css('div#contact-modal input#sku::attr(value)').extract_first()
        price = response.css('div.price-box span.price::text').extract_first().encode('ascii', 'ignore').strip()
        color = response.css('ul.product-colors li.active img::attr(title)').extract_first()
        currency = 'EUR'

        all_sizes = response.css('div.sizebox-wrapper ul li')
        for size in all_sizes:
            size_detail = size.css('::text').extract_first().strip()
            sku_size_id = '{0}_{1}'.format(product_id, size_detail)
            orsay_item['skus'][sku_size_id] = {'price': price, 'color': color, 'currency': currency, 'size': size_detail}
            if size.css('.size-unavailable'):
                orsay_item['skus'][sku_size_id]['out_of_stock'] = True

    def request_another_color_or_yield_item(self, other_color_urls, orsay_item):
        if other_color_urls:
            yield scrapy.Request(other_color_urls.pop(), callback=self.parse_sku_info, meta={
                                                                            'other_color_urls': other_color_urls,
                                                                            'orsay_item': orsay_item})
        else:
            yield orsay_item

    def parse_sku_info(self, response):
        other_color_urls = response.meta['other_color_urls']
        orsay_item = response.meta['orsay_item']
        self.parse_sku_color_info(response,  orsay_item)
        return self.request_another_color_or_yield_item(other_color_urls, orsay_item)

    def parse_orsay_item(self, response):
        orsay_item = OrsayItem()
        orsay_item['brand'] = self.parse_brand_name()
        orsay_item['care'] = self.parse_care_info(response)
        orsay_item['category'] = self.parse_category_info(response)
        orsay_item['description'] = self.parse_description_info(response)
        orsay_item['image_urls'] = []
        orsay_item['name'] = self.parse_item_name(response)
        orsay_item['url'] = self.parse_item_url(response)
        orsay_item['retailer_sku'] = self.parse_retailer_sku_info(response)
        orsay_item['gender'] = self.parse_gender()
        other_color_urls = self.parse_item_other_color_urls(response)
        orsay_item['skus'] = {}
        self.parse_sku_color_info(response, orsay_item)
        return self.request_another_color_or_yield_item(other_color_urls, orsay_item)





