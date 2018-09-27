from scrapy.spiders import Spider
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


from rendezvous_scrapy.items import Product


class RendezvousParseSpider(Spider):
    name = "rendezvous_parser"
    gender_map = [
        ('МАЛЬЧИКАМ', 'boys'),
        ('boys', 'boys'),
        ('ДЕВОЧКАМ', 'girls'),
        ('girls', 'girls'),
        ('МУЖЧИНАМ', 'men'),
        ('Мужские', 'men'),
        ('male', 'men'),
        ('ЖЕНЩИНАМ', 'women'),
        ('Женская', 'women'),
        ('female', 'women')
    ]

    def parse(self, response):
        item = Product()
        item['retailer_sku'] = self.item_retailer_sku(response)
        item['gender'] = self.item_gender(response)
        item['category'] = self.item_category(response)
        item['brand'] = self.item_brand(response)
        item['url'] = response.url
        item['name'] = self.item_name(response)
        item['description'] = self.item_description(response)
        item['care'] = self.item_care(response)
        item['image_urls'] = self.item_image_urls(response)
        item['skus'] = self.item_skus(response)

        return item

    def item_retailer_sku(self, response):
        css = '.media-list::attr(data-model-id)'
        return response.css(css).extract_first()

    def item_gender(self, response):
        soup = f'{self.item_name(response)} {response.url}'
        for token, raw_gender in self.gender_map:
            if token in soup:
                return raw_gender
        return 'unisex-adults'

    def item_category(self, response):
        css = '.breadcrumbs [itemprop="name"]::attr(content)'
        return response.css(css).extract()[1:]

    def item_brand(self, response):
        css = '.item-info .item-name-title a::text'
        return response.css(css).extract_first()

    def item_name(self, response):
        css = '.item-info .item-name-title::text'
        return response.css(css).extract_first()

    def item_care(self, response):
        title_css = '.flex-grid-row dt:contains("материал") span::text,' \
                    ' dt:contains("Материал") span::text'
        title = response.css(title_css).extract()
        care_css = '.flex-grid-row dt:contains("материал") +dd::text,' \
                   ' dt:contains("Материал") +dd::text'
        care = response.css(care_css).extract()
        return [f'{title}: {care}' for title, care in zip(title, care)]

    def item_description(self, response):
        title_css = '#item-features .flex-grid-row :not(:contains("материал")) ' \
                    ':not(:contains("Материал")) span::text'
        title = response.css(title_css).extract()

        des_css = '#item-features .flex-grid-row :not(:contains("материал")) ' \
                  ':not(:contains("Материал")) +dd::text'
        description = response.css(des_css).extract()
        return [f'{title}: {description}' for title, description in zip(title, description)]

    def item_image_urls(self, response):
        css = '.carousel-image-list img::attr(data-src)'
        return response.css(css).extract_first()

    def item_skus(self, response):
        price_css = '.item-info .item-price-new .item-price-value::attr(content)'
        old_p_css = '.item-info .item-price-old .item-price-value::attr(content)'
        colour_css = '.flex-grid-row dt:contains("Цвет") +dd::text'
        colour = response.css(colour_css).extract_first()
        common = {
            'currency': "RUB",
            'colour': colour,
            'price': response.css(price_css).extract_first(),
            'previous_prices': response.css(old_p_css).extract()
        }
        skus = list()
        for size in response.css('.table-of-sizes li::text').extract():
            sku = common.copy()
            sku['size'] = size.strip()
            sku['sku_id'] = f'{colour}_{size.strip()}'
            skus.append(sku)

        return skus


class RendezvousCrawlSpider(CrawlSpider):
    name = "rendezvous"
    allowed_domains = ['yaroslavl.rendez-vous.ru']
    start_urls = [
        'https://yaroslavl.rendez-vous.ru'
    ]
    listings_css = ['#header .nav-link', '.pagination .page.selected+li']
    item_css = ['.item .item-link']
    rules = (
        Rule(LinkExtractor(restrict_css=listings_css)),
        Rule(LinkExtractor(restrict_css=item_css), callback='parse_item'),
    )

    item_parser = RendezvousParseSpider()

    def parse_item(self, response):
        return self.item_parser.parse(response)
