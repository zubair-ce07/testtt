# -*- coding: utf-8 -*-
import re
from urllib import parse

from scrapy import Request, Spider

from scrapy_advance_training.items import ProductItem, SizeInfosItem


class DomeshoppingzoneSpider(Spider):
    name = 'domeshoppingzone'
    allowed_domains = ['domeshoppingzone.com']
    start_urls = ['http://www.domeshoppingzone.com/']

    identifier_re = re.compile('[0-9]{7}')
    color_id_re = re.compile('\w+')
    color_re = re.compile('[a-zA-Z]+')

    def parse(self, response):
        for navigation_url in response.css('.gnavs')[:-1].css('a::attr(href)').extract():
            yield Request(url=response.urljoin(navigation_url), callback=self.parse_items)

    def parse_items(self, response):
        for item_url in response.css('#sectionItemList dt >span >a::attr(href)').extract():
            yield Request(url=response.urljoin(item_url), callback=self.parse_product)

        if not response.meta.get('pagination_done'):
            page_urls = response.css('#sectionItemListHeader li[class=""] a::attr(href)').extract()
            if page_urls:
                page_url = page_urls[-1]
                url_parts = list(parse.urlparse(page_url))
                url_info = dict(parse.parse_qsl(url_parts[4]))
                page_index = int(url_info['PAGE_INDEX'])
                response.meta['pagination_done'] = True
                for index in range(2, page_index+1):
                    url_info['PAGE_INDEX'] = index
                    url_parts[4] = parse.urlencode(url_info)
                    yield Request(parse.urlunparse(url_parts),
                                  self.parse_items,
                                  meta=response.meta)

    def parse_product(self, response):
        product = response.css('#sectionItemInfo')
        old_price, new_price = self.get_prices(product)
        identifier = self.identifier_re.search(response.url).group()

        color = product.css('.unitSelect .colortip img::attr(alt)').extract_first()
        color_id = self.color_id_re.search(color).group()

        return ProductItem(
            available='true',
            url=response.url,
            country_code='jp',
            language_code='ja',
            color_code=color_id,
            base_sku=identifier,
            identifier=identifier,
            old_price_text=old_price,
            new_price_text=new_price,
            full_price_text=new_price,
            brand='Dome Shopping Zone',
            size_infos=self.extract_size(response),
            sku='{}{}'.format(identifier, color_id),
            image_urls=self.get_image_urls(response),
            title=product.css('h1 strong::text').extract_first(),
            referer_url=response.request.headers.get('Referer', ''),
            color_name='/'.join(self.color_re.search(color).group()),
            description_text=product.css(' .unitBlock li::text').extract(),
            category_names=response.css('.breadcrumb li a::text').extract()[1:],
            currency=product.css('.unitItemPrice meta::attr(content)').extract_first()
        )

    @staticmethod
    def get_prices(product_info):
        new_price = product_info.css('.unitItemPrice strong::text').extract_first('')
        if new_price:
            return '', new_price
        price_info = product_info.css('.unitItemPrice strong span::text').extract()
        return price_info[0], price_info[1]

    @staticmethod
    def get_image_urls(response):
        image_urls = response.css('#sectionItemImage .sliderWrap img::attr(src)').extract()
        return [response.urljoin(image_url) for image_url in image_urls]

    @staticmethod
    def extract_size(response):
        return [
            SizeInfosItem(
                stock='in stock',
                size_name=size_info.css('img::attr(alt)').extract_first(),
                size_identifier=size_info.css('input::attr(value)').extract_first(),
            )
            for size_info in response.css('#sectionItemInfo .SIZE li')
        ]
