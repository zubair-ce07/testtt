import json

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider


class Damas(CrawlSpider):
    name = "Damas"
    start_urls = ['http://uae.damasjewellery.com/']
    allows = ['/all-products', '/watches']
    rules = (
        Rule(LinkExtractor(
            restrict_css='.widget>ul>li>a', allow=allows), ),
        Rule(LinkExtractor(
            restrict_css='.page', ), ),
        Rule(LinkExtractor(
            restrict_css='.round-view', ), callback="parse_product"),
        )

    def parse_product(self, response):
        item = {
            'brand': self.get_brand(response),
            'care': [],
            'currency': response.xpath('//meta[@property="product:price:currency"]/@content').extract_first(),
            'category': self.get_category(response),
            'description': self.get_discription(response),
            'gender': self.get_gender(response),
            'img_urls': [response.xpath('//meta[@property="og:image"]/@content').extract_first(), self.get_img_urls(response)],
            'name': response.xpath('//meta[@property="og:title"]/@content').extract_first(),
            'skus': self.get_skus(response),
            'materials': self.get_materials(response),
            'price': response.xpath('//meta[@property="product:price:amount"]/@content').extract_first(),
            'trail': response.css('li.item>a::attr(href)').extract() + [response.request.url],
            'url': response.request.url,
        }
        yield item

    def get_brand(self, response):
        title = response.xpath('//meta[@property="og:title"]/@content').extract_first().split()
        brand = title[0]
        if brand == 'Al':
            brand = title[0] + title[1]
        if brand == 'Tikka':
            brand = title[-1]
        return brand

    def get_category(self, response):
        title = response.xpath('//meta[@property="og:title"]/@content').extract_first().split()
        category = title[-1]
        if category == 'Rangoli':
            category = title[0]
        return category

    def get_discription(self, response):
        descriptions = response.css('.value>p>sapn::text').extract()
        if descriptions:
            description_string = ' '.join(i for i in descriptions if i.strip().encode('ascii', 'ignore'))
            return description_string
        else:
            descriptions = response.css('.value>p::text').extract()
            if descriptions:
                description_string = ' '.join(i for i in descriptions if i.strip().encode('ascii', 'ignore'))
                return description_string
            else:
                descriptions = response.css('.value ::text').extract()
                description_string = ' '.join(i for i in descriptions if i.strip().encode('ascii', 'ignore'))
                return description_string

    def get_gender(self, response):
        brand = self.get_brand(response)
        style_id = response.css('.productSku>p>span::text').extract_first()
        if brand == 'Baraka' and style_id != 'AN271291RBDB026027':
            gender = 'Men'
        else:
            gender = 'Women'
        return gender

    def get_img_urls(self, response):
        script = json.loads(response.xpath('//script[@type="text/x-magento-init"]//text()').extract()[4])
        if script.get('[data-gallery-role=gallery-placeholder]'):
            imgs = script['[data-gallery-role=gallery-placeholder]']['mage/gallery/gallery']
            for img in imgs['data']:
                return img['img']

    def get_materials(self, response):
        materials_list = []
        materials = response.css('.value>p>span>strong::text').extract()[1:]
        for material in materials:
            materials_list.append(material.encode('ascii', 'ignore').strip())
        return materials_list

    def get_skus(self, response):
        sku_list = []
        form = json.loads(response.xpath('//script[@type="text/x-magento-init"]//text()').extract()[6])
        if form.get('#product_addtocart_form',):
            skus = form['#product_addtocart_form']['configurable']['spConfig']['attributes']['174']['options']
            for sku in skus:
                sku_dict = {sku['id']: {
                    'size': sku['label'],
                    'price': response.xpath('//meta[@property="product:price:amount"]/@content').extract_first(),
                    'color': 'One_color',
                }}
                sku_list.append(sku_dict)
            return sku_list
        else:
            return {}
