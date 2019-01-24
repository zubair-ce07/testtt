import json
import re
from urllib.parse import urljoin

from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider, Request

from whitestuff_crawler.items import WhiteStuffCrawlerItem


class WhiteStuffCrawler(CrawlSpider):

    name = 'whitestuff-global-crawl'
    allowed_domains = ['whitestuff.com', 'fsm.attraqt.com']
    start_urls = ['https://www.whitestuff.com/global/sale/',
                  'https://www.whitestuff.com/global/mens/',
                  'https://www.whitestuff.com/global/kids/',
                  'https://www.whitestuff.com/global/sale/',
                  'https://www.whitestuff.com/global/gifts-and-home/',
                  'https://www.whitestuff.com/global/accessories-and-shoes/']

    listings_css = ['.nav-list']
    products_css = ['.product-gridlist .product-tile .product-tile__image']

    rules = (Rule(LinkExtractor(restrict_css=listings_css), callback='parse_sub_category'),
             Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'))

    def parse_sub_category(self, response):
        domains = response.url.split('//')[-1].split('/')
        category = domains[2]
        sub_category = domains[3]

        css = 'script:contains("LM.DisableAutoInitialize") ::text'
        conf_categorytree = response.css(css).re_first('categorytree = \"(.*)\"')
        conf_category = response.css(css).re_first('category= \"(.*)\"')

        next_url = f"""https://fsm.attraqt.com/zones-js.aspx?siteId=c7439161-d4f1-4370-939b-ef33f4c876cc&
        referrer=https%3A%2F%2Fwww.whitestuff.com%2Fglobal%2Fwomens%2Fknitwear%2F%3Fesp_viewall%3Dy%255C&
        sitereferrer=&pageurl=https%3A%2F%2Fwww.whitestuff.com%2Fglobal%2F{category}%2F{sub_category}
        ?esp_pg={0}&zone0=banner&zone1=category&zone2=advert1&zone3=advert2&zone4=advert3&facetmode=html&
        mergehash=false&culture=en-US&currency=USD&language=en-GB&config_categorytree={conf_categorytree}&
        config_category={conf_category}&config_region=WhiteStuff_ROW&config_brand=null&config_colour=null&
        config_producttype=null&config_fsm_sid=e7ef7d94-5868-450c-dc9a-bcf75d283498"""

        yield Request(url=next_url, callback=self.parse_pagination, meta={'category': category, 'sub_category':
                        sub_category, 'conf_categorytree': conf_categorytree, 'conf_category': conf_category})

    def parse_pagination(self, response):
        page_size = 24
        page_number = 1

        yield from self.parse_products(response)

        category = response.meta['category']
        sub_category = response.meta['sub_category']
        conf_categorytree = response.meta['conf_categorytree']
        conf_category = response.meta['conf_category']

        raw_data = re.findall('"html":"(.*)}', response.text)[0]
        sel = Selector(text=str(raw_data))

        products = sel.css('span ::attr(data-hitcount)').extract_first()
        products = re.search('\d+', products).group(0)

        for page in range(1, int(products), page_size):
            next_url = f"""https://fsm.attraqt.com/zones-js.aspx?siteId=c7439161-d4f1-4370-939b-ef33f4c876cc&
            referrer=https%3A%2F%2Fwww.whitestuff.com%2Fglobal%2Fwomens%2Fknitwear%2F%3Fesp_viewall%3Dy%255C&
            sitereferrer=&pageurl=https%3A%2F%2Fwww.whitestuff.com%2Fglobal%2F{category}%2F{sub_category}?
            esp_pg={page_number}&zone0=banner&zone1=category&zone2=advert1&zone3=advert2&zone4=advert3&
            facetmode=html&mergehash=false&culture=en-US&currency=USD&language=en-GB&config_categorytree=
            {conf_categorytree}&config_category={conf_category}&config_region=WhiteStuff_ROW&config_brand=null&
            config_colour=null&config_producttype=null&config_fsm_sid=e7ef7d94-5868-450c-dc9a-bcf75d283498"""

            page_number += 1
            yield Request(url=next_url, callback=self.parse_products)

    def parse_products(self, response):
        base_url = 'https://www.whitestuff.com/'
        sel = Selector(text=str(re.findall('html":"(.*)}', response.text)[0].replace('\\', '')))

        for rel_url in sel.css('.product-tile .product-tile__title a::attr(href)').extract():
            yield Request(url=urljoin(base_url, rel_url), callback=self.parse_product_detail)

    def parse_product_detail(self, response):
        item = WhiteStuffCrawlerItem()

        item['lang'] = 'en'
        item['market'] = 'UK'
        item['brand'] = 'whitestuff'
        item['url'] = self.product_url(response)
        item['care'] = self.product_care(response)
        item['name'] = self.product_name(response)
        item['skus'] = self.product_skus(response)
        item['gender'] = self.product_gender(response)
        item['category'] = self.product_category(response)
        item['image_urls'] = self.product_image_urls(response)
        item['description'] = self.product_description(response)
        item['retailer_sku'] = self.product_retailer_sku(response)
        return item

    def product_skus(self, response):
        colours = self.product_colours(response)
        return [self.skus(response, colour) for colour in colours]

    def skus(self, response, colour):
        skus = {}
        sizes_css = '.product-details__info .form-control.js-variation-attribute.' \
                    'product-form-variation__attr.product-form-variation__attr--size option'

        common_sku = self.product_pricing(response)
        common_sku['colour'] = colour

        for size_s in response.css(sizes_css):
            size = size_s.css('option ::attr(value)').extract_first()

            if size:
                sku = common_sku.copy()
                sku['size'] = size
                if size_s.css('a::attr(disabled)'):
                    sku['out_of_stock'] = True
                skus[f'{colour}_{size}'] = sku
        return skus

    def product_url(self, response):
        return response.url

    def product_name(self, response):
        css = '.product-info__inner .product-info__heading ::text'
        return response.css(css).extract_first()

    def product_gender(self, response):
        return json.loads(self.product_category(response))[0]

    def product_category(self, response):
        css = 'script:contains("siteSubSection") ::text'
        return response.css(css).re_first('"siteSubSection": (\[.*),')

    def product_retailer_sku(self, response):
        css ='.product-details__info .product-info__product-id span::text'
        return response.css(css).extract_first()

    def product_care(self, response):
        return response.css('.ish-ca-value::text').extract()

    def product_image_urls(self, response):
        css = '.lazyload--blur-up ::attr(src)'
        return response.css(css).extract()

    def product_colours(self, response):
        css = '.product-details .product-swatches a::attr(data-variation-value)'
        return response.css(css).extract()

    def product_description(self, response):
        css = '.product-info__desc.js-lineclamp::text'
        return response.css(css).extract_first()

    def product_pricing(self, response):
        prev_price_css = '.product-details__info .old-price s::text'
        price_css = '.product-details__info .current-price meta::attr(content)'

        price_and_currency = response.css(price_css).extract()
        prev_price = response.css(prev_price_css).extract_first()

        pricing = {'price': price_and_currency[0]}
        pricing['currency'] = price_and_currency[1]

        if prev_price:
            pricing['previous_price'] = prev_price

        return pricing
