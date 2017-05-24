from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from OspraySpider.items import OrsayspiderItem
from scrapy import Request


class OrsaySpider(CrawlSpider):
    name = "osray"
    allowed_domains = ["orsay.com"]
    start_urls = ["http://www.orsay.com/de-de"]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('li.level1 > a',)), follow=True),
        Rule(LinkExtractor(allow=(), restrict_css=('ul.products-list > li.item > article > div > a',)),
             callback="parse_items",
             follow=True)
    )

    def parse_items(self, response):
        links = response.css('ul.product-colors>li>a::attr(href)').extract()[1:]
        if links:
            request = Request(links[0], callback=self.parse_additional_colors)
            request.meta['care'] = self.get_care(response)
            request.meta['description'] = [self.get_description(response)]
            request.meta['image_urls'] = [self.get_image(response)]
            request.meta['name'] = [self.get_product_name(response)]
            request.meta['retailer_sku'] = self.get_sku(response)[:-2]
            request.meta['skus'] = self.get_skus(response)
            request.meta['url'] = response.url
            request.meta['url_original'] = response.url
            request.meta['links'] = links[1:]
            return request
        else:
            item = OrsayspiderItem()
            item.setdefault('brand', 'Osray')
            item.setdefault('gender', 'female')
            item.setdefault('category', [])
            item['care'] = self.get_care(response)
            item['description'] = [self.get_description(response)]
            item['image_urls'] = [self.get_image(response)]
            item['name'] = [self.get_product_name(response)]
            item['retailer_sku'] = self.get_sku(response)[:-2]
            item['skus'] = self.get_skus(response)
            item['url'] = response.url
            item['url_original'] = response.url
            return item

    def parse_additional_colors(self, response):
        links = response.meta['links']
        skus = response.meta['skus']
        skus.update(self.get_skus(response))
        image_urls = response.meta['image_urls']
        image_urls.append(self.get_image(response))
        if links:
            request = Request(links[0], callback=self.parse_additional_colors)
            request.meta['care'] = response.meta['care']
            request.meta['description'] = response.meta['description']
            request.meta['image_urls'] = image_urls
            request.meta['name'] = response.meta['name']
            request.meta['retailer_sku'] = response.meta['retailer_sku']
            request.meta['skus'] = skus
            request.meta['url'] = response.meta['url']
            request.meta['url_original'] = response.meta['url_original']
            request.meta['links'] = links[1:]
            return request
        else:
            item = OrsayspiderItem()
            item.setdefault('brand', 'Osray')
            item.setdefault('gender', 'female')
            item.setdefault('category', [])
            item['care'] = response.meta['care']
            item['description'] = response.meta['description']
            item['image_urls'] = image_urls
            item['name'] = response.meta['name']
            item['retailer_sku'] = response.meta['retailer_sku']
            item['skus'] = skus
            item['url'] = response.meta['url']
            item['url_original'] = response.meta['url_original']
            return item

    def get_skus(self, response):
        sku = self.get_sku(response)
        sizes = self.get_sizes(response)
        price = self.get_price(response)
        currency_codes = {'$': 'DOL', '€': 'EUR', '£': 'POU'}
        currency = currency_codes[price[-1]]
        price_literals = ""
        result = {}
        for i in price:
            if i.isdigit():
                price_literals += i
        for k in sizes:
            if 'Unavailable' in k:
                formatted_size = k.strip('Unavailable-')
                result['{0}_{1}'.format(sku, formatted_size)] = {
                    'colour': self.get_current_color(response),
                    'currency': currency,
                    'out_of_stock': True,
                    'price': int(price_literals),
                    'size': formatted_size
                }
            else:
                result['{0}_{1}'.format(sku, k)] = {
                    'colour': self.get_current_color(response),
                    'currency': currency,
                    'price': int(price_literals),
                    'size': k
                }
        return result

    def get_care(self, response):
        care = []
        for care_item in response.css('p.material::text, ul.caresymbols > li > img::attr(src)').extract():
            care.append(care_item)
        return care

    def get_description(self, response):
        desc = response.css('p.description::text').extract_first()
        desc = desc.strip()
        return desc

    def get_image(self, response):
        return response.css('#mainZoom::attr(href)').extract_first()

    def get_colors(self, response):
        return response.css('ul.product-colors>li>a>img::attr(title) ').extract()

    def get_current_color(self, response):
        return response.css('ul.product-colors>li>a>img::attr(title) ').extract_first()

    def get_color_url_list(self, response):
        return (response.css('ul.product-colors>li>a::attr(href)').extract())[1:]

    def get_sku(self, response):
        return response.css('#sku::attr(value)').extract_first()

    def get_product_name(self, response):
        return response.css('h1.product-name::text').extract_first()

    def get_price(self, response):
        return response.css('div.price-box span.price::text').extract_first().strip()

    def get_sizes(self, response):
        sizes = []
        for k in response.css('div.sizebox-wrapper > ul > li::text').extract():
            k = k.strip()
            if k:
                sizes.append(k)
            else:
                sizes[-1] = 'Unavailable-{}'.format(sizes[-1])
        return sizes
