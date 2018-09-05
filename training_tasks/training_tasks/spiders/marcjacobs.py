# -*- coding: utf-8 -*-
from json import loads
from urllib import parse

from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from training_tasks.items import ProductItem, SkuItem


class MarcjacobsSpider(CrawlSpider):
    name = 'marcjacobs'
    allowed_domains = ['marcjacobs.com', 'i1.adis.ws']
    start_urls = ['https://www.marcjacobs.com/']

    image_url_t = 'https://i1.adis.ws/s/Marc_Jacobs/{}_{}_SET.js' \
                  '?func=app.mjiProduct.handleJSON&amp;protocol=https'

    size_key_t = 'dwvar_{}_size'
    color_key_t = 'dwvar_{}_color'

    navigation_css = '#navigation li.mobile-hidden a'
    products_css = '.search-result-items div >a'
    rules = (
        Rule(LinkExtractor(restrict_css=navigation_css), follow=True),
        Rule(LinkExtractor(restrict_css=products_css), callback='parse_product'),
    )

    def parse_product(self, response):
        product_item = self.get_product_basic_info(response)
        color_variants = [
            (
                color_variant.css('::attr(href)').extract_first(),
                color_variant.css('::text').extract_first()
            )
            for color_variant in response.css('.product-variations .swatches a')
        ]
        yield self.make_request_for_color(product_item, color_variants)

    def make_request_for_color(self, product_item, color_variants):
        if color_variants:
            color_url = color_variants.pop()
            meta = {'item': product_item, 'color': color_url[1], 'color_variants': color_variants}
            return Request(url=color_url[0], callback=self.parse_color, meta=meta, dont_filter=True)
        else:
            return product_item

    def parse_color(self, response):
        product_item = response.meta['item']
        product_id = self.get_id(response.url, 'pid')
        color_id = self.get_id(response.url, self.color_key_t.format(product_id))

        self.extract_sku_items(product_id, color_id, product_item, response)
        url = self.image_url_t.format(product_id, color_id)
        response.meta.update({'item': product_item})
        yield Request(url=url, callback=self.parse_image_urls, meta=response.meta, dont_filter=True)

    def parse_image_urls(self, response):
        product_item = response.meta['item']
        image_url_info = response.text.replace('app.mjiProduct.handleJSON(', '').replace(');', '')
        image_url_info = loads(image_url_info)
        product_item['image_urls'] += [image_item['src'] for image_item in image_url_info['items']]
        return self.make_request_for_color(product_item,response.meta['color_variants'])

    def extract_sku_items(self, product_id, color_id, product_item, response):
        currency_css = 'meta[property="product:price:currency"]::attr(content)'
        currency = response.css(currency_css).extract_first('')

        price_css = 'meta[property="product:price:amount"]::attr(content)'
        price = response.css('.product-price span::text').extract_first('').strip()
        price = response.css(price_css).extract_first(price)

        stock = response.css('meta[property="og:availability"]::attr(content)').extract_first('')

        size_urls = response.css('#va-size option::attr(value)').extract()
        for size_url in size_urls:
            if size_url:
                size_key = self.size_key_t.format(product_id)

                sku_item = SkuItem(
                    stock=stock,
                    price=price,
                    currency=currency,
                    color=response.meta['color'],
                    size=self.get_id(size_url, size_key),
                )
                sku_id = self.get_sku_id(size_url, color_id)
                product_item['skus'].update({sku_id: sku_item})

    def get_product_basic_info(self, response):
        description_css = 'meta[property="og:description"]::attr(content)'
        category = response.css('input[name="categorytype"]::attr(value)').extract_first()
        sub_category = response.css('input[name="subCategoryName"]::attr(value)').extract_first()

        return ProductItem(
            care='',
            skus={},
            image_urls=[],
            url=response.url,
            original_url=response.url,
            retailer_sku=self.get_retailer_sku(response.url),
            category='{}-{}'.format(category, sub_category),
            description=response.css(description_css).extract_first(),
            name=response.css('h1.product-name::text').extract_first(),
            brand=response.css('meta[property="og:brand"]::attr(content)').extract_first(),
        )

    def get_sku_id(self, size_link, color_id):
        pid = self.get_id(size_link, 'pid')
        size_key = self.size_key_t.format(pid)
        size_id = self.get_id(size_link, size_key)
        return '{}{}_{}'.format(pid, color_id, size_id)

    @staticmethod
    def get_retailer_sku(page_url):
        url_parse = parse.urlparse(page_url)
        return url_parse.path.split('/')[-1].replace('.html', '')

    @staticmethod
    def get_id(link, param):
        url_parse = parse.urlparse(link)
        param_dictionary = dict(parse.parse_qsl(url_parse.query))
        return param_dictionary.get(param, '')
