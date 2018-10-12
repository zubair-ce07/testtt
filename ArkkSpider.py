import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class ArkkSpider(CrawlSpider):
    name = "ArkkSpider"
    base_url = ['https://www.arkkcopenhagen.com']
    start_urls = ['https://www.arkkcopenhagen.com']

    rules = (
        Rule(LinkExtractor(
            restrict_css='a.btn'), ),
        Rule(LinkExtractor(
            restrict_css='a.grid-view-item__link.grid-view-item__image-container'), callback="parse_product"),)

    def parse_product(self, response):
        item = {
            'brand': response.css('.analytics').re_first('"brand":"(.*?)",'),
            'care': None,
            'care_instructions': None,
            'category': response.css('.analytics').re_first('"category":"(.*?)",'),
            'currency': response.xpath('//meta[@property="og:price:currency"]/@content').extract_first(),
            'description': response.css('.product-single__description>p::text').extract_first(),
            'gender': response.css('.product-single__sizing-title::text').extract_first()[0:-7],
            'img-urls': self.get_img_urls(response),
            'name': response.css('.product-single__title::text').extract_first(),
            'skus': self.get_skus(response),
            'material': self.get_materials(response),
            'trail': self.get_trail(response),
            'url': response.request.url,
        }
        yield item

    def get_trail(self,response):
        trail_list = []
        trails = response.css('.breadcrumb>a::attr(href)').extract()
        for trail in trails:
            trail_url = response.urljoin(trail)
            trail_list.append(trail_url)
        return trail_list

    def get_img_urls(self, response):
        imgs_urls_list = []
        main_img_url = response.urljoin(response.css('.feature-row__image::attr(src)').extract_first())
        imgs_urls_list.append(main_img_url)
        urls_list = response.css('.product-single__thumbnail-image::attr(src)').extract()
        for url in urls_list:
            img_url = response.urljoin(url)
            imgs_urls_list.append(img_url)
        return imgs_urls_list

    def get_skus(self, response):
        skus_list = []
        meta = json.loads(response.css('script::text').re_first('var meta = ({.+});'))
        skus = meta['product']
        for sku in skus['variants']:
            sku_dict = {sku['id']: {
                'name': sku['name'],
                'price': sku['price'],
                'size': sku['public_title'][-2:],
                'color': sku['public_title'][0:-6],
            }}
            skus_list.append(sku_dict)
        return skus_list

    def get_materials(self, response):
        materials_list = []
        materials = response.css('.split-section__text::text').extract()[1:-4]
        for material in materials:
            materials_list.append(material.strip().strip("-"))
        return materials_list
