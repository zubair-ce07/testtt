# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import json

from scrapy import Request, Spider

from training_tasks.items import ProductItem, SkuItem


class CasallSpider(Spider):
    name = 'casall_spider'
    allowed_domains = ['casall.com']
    start_urls = ['https://www.casall.com/us/']

    def parse(self, response):
        navigation = response.css('ul[data-dropdownmenu] li>a::attr(href)').extract()
        for nav_url in navigation:
            if '/us/inspiration' not in nav_url:
                nav_url = response.urljoin(nav_url)
                yield Request(url=nav_url, callback=self.parse_product_list)

    def parse_product_list(self, response):
        if not self.is_available(response):
            return

        urls = set(response.css('div[data-productlist] .product-list a::attr(href)').extract())
        for url in urls:
            url = response.urljoin(url)
            yield Request(url=url, callback=self.parse_product)

        next_page_url = response.css('li.next a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield Request(url=next_page_url, callback=self.parse_product_list)

    def parse_product(self, response):
        if not self.is_available(response):
            return

        product_item = self.get_product_basic_info(response)

        product_info = response.css('div.product-info')[0]
        variant_color_urls = product_info.css('ul.variant-color li a::attr(href)').extract()
        variant_color_urls = [response.urljoin(url) for url in variant_color_urls]

        if not variant_color_urls:
            variant_color_urls.append(response.url)

        yield from self.make_requests_for_color(product_item, variant_color_urls)

    def make_requests_for_color(self, product_item, color_urls):
        if color_urls:
            yield Request(
                url=color_urls.pop(),
                callback=self.parse_color,
                meta={'item': product_item, 'color_urls': color_urls},
                dont_filter=True
            )
        else:
            yield product_item

    def parse_color(self, response):
        product_item = response.meta['item']
        product_item['image_urls'] += self.get_image_urls(response)
        
        size_options = response.css('select.variant-size option')
        size_variant_urls = [self.get_item_size_url(option) for option in size_options]
        yield from self.make_request_for_size(product_item, size_variant_urls, response)

    def make_request_for_size(self, product_item, size_variant_urls, response):
        meta = response.meta
        if size_variant_urls:
            size_url = size_variant_urls.pop()
            url = response.urljoin(size_url[0])
            meta.update({
                'item': product_item,
                'size': size_url[1],
                'size_variant_urls': size_variant_urls
            })
            yield Request(url=url, callback=self.parse_size, meta=meta, dont_filter=True)
        else:
            yield from self.make_requests_for_color(product_item, meta['color_urls'])

    def parse_size(self, response):
        product_item = response.meta['item']

        product_info = response.css('div.product-info')[0]
        price_stock_info = json.loads(product_info.css('::attr(data-gtm)').extract_first({}))
        price_info = response.css('div.price-info span[itemprop="price"]::text')
        price_info = price_info.extract_first('').strip()
        product_color = product_info.css('h1::text').extract_first('')

        sku_item = SkuItem(
            price=price_stock_info.get('price', price_info),
            size=response.meta['size'],
            color=product_color.split(' – ')[1],
            currency=response.css('meta[itemprop]::attr(content)').extract_first(''),
            stock=price_stock_info.get('dimension1', '')
        )

        sku_id = self.get_sku_id(response.url, response.meta['size'])
        product_item['skus'].update({sku_id: sku_item})

        urls = response.meta['size_variant_urls']
        yield from self.make_request_for_size(product_item, urls, response)

    @staticmethod
    def get_product_basic_info(response):
        """This function return product  item filled with basic information"""
        product_info = response.css('div.product-info')[0]
        description = product_info.css('div.columns.description p::text').extract_first('').strip()
        material = product_info.css('div.columns.material p::text').extract_first('').strip()
        care = product_info.css('div.columns.careinstruction p::text').extract_first('').strip()
        item_data = json.loads(product_info.css('::attr(data-gtm)').extract_first())

        return ProductItem(
            brand='casall',
            care=[material, care],
            description=description,
            category=item_data['category'],
            name=item_data['name'],
            retailer_sku=item_data['id'],
            skus={},
            image_urls=[],
            original_url=response.url
        )

    @staticmethod
    def get_image_urls(response):
        image_links = response.css('li.thumbnail img::attr(src)').extract()
        return [response.urljoin(image_link) for image_link in image_links]

    @staticmethod
    def get_sku_id(link, size):
        return '-'.join((link.split('-')[-1], size))

    @staticmethod
    def get_item_size_url(option):
        url = option.css('::attr(value)').extract_first('')
        size = option.css('::text').extract_first('').strip().replace(' (Out of stock)', '')
        return url, size

    @staticmethod
    def is_available(response):
        """Products are available are not"""
        availability_msg = response.css('p[style="color:red"]::text').extract_first('')
        return 'not currently available' in availability_msg
