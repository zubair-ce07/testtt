import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrape_orsay.items import OrsayItem


class OrsaySpider(CrawlSpider):
    name = "orsay_spider"
    start_urls = ['http://www.orsay.com/de-de/']
    orsay_product_ids = []

    rules = (
        Rule(LinkExtractor(restrict_css=('div#topMenu-container a',))),
        Rule(LinkExtractor(restrict_css=('div.pages li.arrow a',))),
        Rule(LinkExtractor(restrict_css=('div.product-shop a',)), callback='parse_orsay_item'),
             )

    def already_scraped(self,response):
        orsay_item_id = response.css('div#contact-modal input#sku::attr(value)').extract_first()
        return orsay_item_id in self.orsay_product_ids

    def parse_care_info(self, response):
        material = response.css('div.product-care p.material::text').extract_first()
        care_images = response.css('div.product-care ul.caresymbols img::attr(src)').extract()
        return [material] + care_images

    def parse_sku_info(self, response):
        other_urls = response.meta['other_urls']
        skus_data = response.meta['skus_data']
        orsay_item = response.meta['orsay_item']

        orsay_item['image_urls'].append(response.css('div.product-image-gallery a::attr(href)').extract_first())
        product_id = response.css('div#contact-modal input#sku::attr(value)').extract_first()
        price = response.css('div.price-box span.price::text').extract_first().encode('ascii', 'ignore')
        color = response.css('ul.product-colors li.active img::attr(title)').extract_first()
        currency = 'EUR'

        all_sizes = response.css('div.sizebox-wrapper ul li')
        for size in all_sizes:
            size_detail = size.css('::text').extract_first().strip()
            sku_size_id = '{0}_{1}'.format(product_id, size_detail)
            skus_data[sku_size_id] = {'price': price, 'color': color, 'currency': currency, 'size': size_detail}
            if size.css('.size-unavailable'):
                skus_data[sku_size_id]['out_of_stock'] = True

        if other_urls:
            yield scrapy.Request(other_urls.pop(), dont_filter=True,
                                 callback=self.parse_sku_info,
                                 meta={'skus_data': skus_data,
                                       'other_urls': other_urls,
                                       'orsay_item': orsay_item})
        else:
            orsay_item['skus'] = skus_data
            yield orsay_item

    def parse_orsay_item(self, response):
        if self.already_scraped(response):
            return
        else:
            self.orsay_product_ids.append(response.css('div#contact-modal input#sku::attr(value)').extract_first())
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
            skus_urls = response.css('ul.product-colors li a::attr(href)').extract()
            skus_urls = skus_urls[1:]
            skus_data = {}
            yield scrapy.Request(response.url, dont_filter=True, callback=self.parse_sku_info, meta={
                                                                                'skus_data': skus_data,
                                                                                'other_urls': skus_urls,
                                                                                'orsay_item': orsay_item})





