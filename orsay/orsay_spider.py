import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrape_orsay.items import OrsayItem


class OrsaySpider(CrawlSpider):
    name = "orsay_spider"
    allowed_domains = ["orsay.com"]
    start_urls = ['http://www.orsay.com/de-de/neuheiten/t-shirts/kurzarm.html']

    rules = (
            Rule(LinkExtractor(restrict_css=('div#topMenu-container a',))),
            Rule(LinkExtractor(restrict_css=('div.pages li.arrow a',))),
            Rule(LinkExtractor(restrict_css=('div.product-shop a',)), callback='parse_orsay_item'),
        )

    def parse_care_info(self, response):
        material = response.css('div.product-care p.material::text').extract_first()
        care_images = response.css('div.product-care ul.caresymbols img::attr(src)').extract()
        return [material] + care_images

    def parse_sku_color_info(self, response, skus_data, orsay_item):
        orsay_item['image_urls'].append(response.css('div.product-image-gallery a::attr(href)').extract_first())
        product_id = response.css('div#contact-modal input#sku::attr(value)').extract_first()
        price = response.css('div.price-box span.price::text').extract_first().encode('ascii', 'ignore').strip()
        color = response.css('ul.product-colors li.active img::attr(title)').extract_first()
        currency = 'EUR'

        all_sizes = response.css('div.sizebox-wrapper ul li')
        for size in all_sizes:
            size_detail = size.css('::text').extract_first().strip()
            sku_size_id = '{0}_{1}'.format(product_id, size_detail)
            skus_data[sku_size_id] = {'price': price, 'color': color, 'currency': currency, 'size': size_detail}
            if size.css('.size-unavailable'):
                skus_data[sku_size_id]['out_of_stock'] = True

    def parse_sku_info(self, response):
        other_color_urls = response.meta['other_color_urls']
        skus_data = response.meta['skus_data']
        orsay_item = response.meta['orsay_item']
        self.parse_sku_color_info(response, skus_data, orsay_item)
        if other_color_urls:
            yield scrapy.Request(other_color_urls.pop(),
                                 callback=self.parse_sku_info,
                                 meta={
                                    'skus_data': skus_data,
                                    'other_color_urls': other_color_urls,
                                    'orsay_item': orsay_item})
        else:
            orsay_item['skus'] = skus_data
            yield orsay_item

    def parse_orsay_item(self, response):
        orsay_item = OrsayItem()
        orsay_item['brand'] = 'Orsay'
        orsay_item['care'] = self.parse_care_info(response)
        orsay_item['category'] = response.css('div.product-view input[name="category_name"]::attr(value)').extract_first()
        orsay_item['description'] = [response.css('div.product-info-and-care p.description::text').extract_first().strip()]
        orsay_item['image_urls'] = []
        orsay_item['name'] = response.css('div.product-essential .product-name::text').extract_first()
        orsay_item['url'] = response.url
        orsay_item['retailer_sku'] = response.css('div#contact-modal input#sku::attr(value)').extract_first()[:-2]
        orsay_item['gender'] = 'women'
        other_color_urls = response.css('ul.product-colors li a::attr(href)').extract()[1:]
        skus_data = {}
        self.parse_sku_color_info(response, skus_data, orsay_item)
        if other_color_urls:
            yield scrapy.Request(other_color_urls.pop(), callback=self.parse_sku_info, meta={
                                                                            'skus_data': skus_data,
                                                                            'other_color_urls': other_color_urls,
                                                                            'orsay_item': orsay_item})
        else:
            orsay_item['skus'] = skus_data
            yield orsay_item



