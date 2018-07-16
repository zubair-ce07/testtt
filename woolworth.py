import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class WoolworthSpider(CrawlSpider):
    name = 'woolworths'
    allowed_domains = ['woolworths.co.za']
    start_urls = ['https://woolworths.co.za']
    download_delay = 3

    rules = (
        Rule(LinkExtractor(restrict_css=['.main-nav__list-item--secondary .main-nav__link',
                                         '.pagination'])),
        Rule(LinkExtractor(restrict_css='.product-card__visual'), callback='parse_products')
    )

    def parse_products(self, response):
        resp = response.css('body > script::text')[0].extract()
        json_resp = json.loads(resp.split('= ')[1])
        item = {
            'description': self.description(response),
            'type': self.product_type(json_resp),
            'image_url': self.image_url(json_resp),
            'product_name': self.product_name(json_resp),
            'sku': self.sku_id(json_resp),
            'url': response.url,
            'skus': self.populate_sku_for_all_sizes(json_resp)
        }
        yield item

    def populate_sku_for_all_sizes(self, json_resp):
        items = {
            'skus': {}
        }
        price = self.price(json_resp)
        for col in self.colors(json_resp):
            for size in self.sizes(json_resp):
                values = {
                    'color': col,
                    'price': price,
                    'size': size
                }
                items['skus']['{0}_{1}_{2}'.format(self.sku_id(json_resp), size, col)] = values
            return items['skus']

    def product_type(self, response):
        prod_type = (response['pdp']['productInfo']['breadcrumbs']['default'])
        return [d[k] for d in prod_type for k in d if k == 'label']

    def colors(self, response):
        color = (response['pdp']['productInfo']['colourSKUs'])
        return [d[k] for d in color for k in d if k == 'colour']

    def price(self, json_resp):
        return json_resp['pdp']['productPrices'][self.sku_id(json_resp)]['plist3620008']['priceMax']

    def sizes(self, response):
        size = (response['pdp']['productInfo']['styleIdSizeSKUsMap']).values()[0]
        return [d[k] for d in size for k in d if k == 'size']

    def image_url(self, response):
        url = (response['pdp']['productInfo']['colourSKUs'])
        image_url = [d[k] for d in url for k in d if k == 'externalImageUrlReference']
        return ['https://woolworths.co.za/{0}'.format(image) for image in image_url]

    def description(self, response):
        return ' '.join(t.strip() for t in response.css('.accordion--chrome .accordion__segment--chrome > '
                                                        'div ::text').extract()[:-2]).strip()

    def sku_id(self, response):
        return response['pdp']['productInfo']['productId']

    def product_name(self, response):
        return response['pdp']['productInfo']['displayName']
