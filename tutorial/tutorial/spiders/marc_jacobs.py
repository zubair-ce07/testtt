#!/usr/bin/env python3
import re
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from .product import MarcJacobProduct
from termcolor import colored


class MarcJacobsSpider(CrawlSpider):
    name = "marcjacobs_spider"

    start_urls = ['https://www.marcjacobs.com/']

    rules = (
        Rule(LxmlLinkExtractor(restrict_css=[
            'a[title="NEW ARRIVALS"]']),
            follow=True),
        # Rule(LinkExtractor(restrict_css=[
        #         'li.mobile-hidden div.level-2 ul.level-3 a'])),
        # Rule(LinkExtractor(restrict_css=[
        #         'li.mobile-hidden div.level-2 ul.menu-vertical a'])),
        # Rule(LinkExtractor(restrict_css=[
        #         'li.mobile-hidden:first-of-type a'])),
        # Rule(LinkExtractor(restrict_css=['a.product-page-link'],
        #                    attrs=('href',),
        #                    callback='parse_product_page')),
        Rule(
            LxmlLinkExtractor(
                restrict_css='div.product-tile.needsclick',
                # attrs=('data-href',)
                # tags=('div')
            ),
            callback='parse_product_page'),
    )

    def next_color_request(
            self, response, color_requests,
            size_requests, image_requests, product):

        next_color_request = self.single_color_request(
            color_requests)
        return response.follow(
            next_color_request['color_url'] + '&Quantity=1&format=ajax',
            self.parse_color_of_product_page,
            meta={
                'product': product,
                'color_name': next_color_request['color'],
                'remaining_color_requests': color_requests,
                'remaining_size_requests': size_requests,
                'image_sources': image_requests,
            }
        )

    def next_image_request(
            self, response, color_requests,
            size_requests, image_requests, product):
        path_to_images = image_requests.pop(0)
        return response.follow(
            path_to_images,
            self.parse_images,
            meta={
                'product': product,
                'image_sources': image_requests
            })

    def next_size_request(
            self, response, color_requests,
            size_requests, image_requests, product):
        next_size_request = self.single_size_request(size_requests)
        return response.follow(
            next_size_request['size_url'] + '&Quantity=1&format=ajax',
            self.parse_color_size_product_page,
            meta={
                'size': next_size_request['size'],
                'remaining_size_requests': size_requests,
                'product': product,
                'color_name': next_size_request['color'],
                'image_sources': image_requests
            })

    def next_request(
            self, response, color_requests,
            size_requests, image_requests, product):
        if color_requests:
            return self.next_color_request(
                response, color_requests, size_requests, image_requests,
                product)
        elif size_requests:
            return self.next_size_request(
                response, color_requests, size_requests, image_requests,
                product)
        elif image_requests:
            return self.next_image_request(
                response, color_requests, size_requests, image_requests,
                product)
        else:
            return product

    def parse_product_page(self, response):

        product = MarcJacobProduct(
            product_id=self.product_id(response),
            product_name=self.get_product_name(response),
            product_category=self.get_product_category(response),
            source_url=response.url,
            images=[],
            skus=[]
        )

        return self.next_request(
            response, self.color_requests(response), [], [], product)

    def parse_color_of_product_page(self, response):
        response.meta['remaining_size_requests'].extend(self.size_requests(
            response.meta['color_name'], response))
        response.meta['image_sources'].append(self.image_paths(response))
        return self.next_request(
            response,
            response.meta['remaining_color_requests'],
            response.meta['remaining_size_requests'],
            response.meta['image_sources'],
            response.meta['product'])

    def parse_color_size_product_page(self, response):

        response.meta['product']['skus'].append(self.product_sku(response))
        return self.next_request(
            response,
            [],
            response.meta['remaining_size_requests'],
            response.meta['image_sources'],
            response.meta['product'])

    def parse_images(self, response):
        images = json.loads(response.text[26:-2])
        response.meta['product']['images'].extend(
            x['src'] for x in images['items'])
        return self.next_request(response,
                                 [],
                                 [],
                                 response.meta['image_sources'],
                                 response.meta['product'])

    def get_product_category(self, response):
        return response.css('a.breadcrumb-element::text').extract()

    def get_product_name(self, response):
        return response.css(
            'h1.product-name::text').extract_first()

    def get_size_options(self, response):
        options = response.css(
            'select#va-size option[value!=""]::text').extract()
        return list(map(str.strip, options))

    def color_requests(self, selector):
        comibnations = []
        for color_tag in selector.css(
                'a[class="swatchanchor"]'):
            color_url = color_tag.css('::attr(href)').extract_first()
            color = color_tag.css('::text').extract_first()
            comibnations.append({'color': color, 'color_url': color_url})
        return comibnations

    def size_requests(self, color, selector):
        comibnations = []

        for size_tag in selector.css(
                'select[id="va-size"] option[value!=""]'):
            if not selector.css(
                    'li.variant-dropdown.double[style="display: none;"]'):
                size = None
            else:
                size = size_tag.css('::text').extract_first().strip('\n')
            size_url = size_tag.css('::attr(value)').extract_first()
            comibnations.append(
                {'size': size, 'size_url': size_url, 'color': color})
        return comibnations

    def single_size_request(self, remaining_size_requests):
        if remaining_size_requests:
            return remaining_size_requests.pop(0)
        return None

    def single_color_request(self, remaining_color_requests):
        if remaining_color_requests:
            return remaining_color_requests.pop(0)
        return None

    def product_sku(self, response):
        size_color = response.meta['color_name']
        quantity_of_product = self.product_quantity(response)
        availability = True if quantity_of_product else False
        price_of_size = self.price_of_size(response)

        return {
            'color': size_color,
            'price': price_of_size,
            'size': response.meta['size'],
            'availability': availability
        }

    def price_of_size(self, selector):
        price = selector.css(
            'span[itemprop="price"]::attr(content)').extract_first()
        return re.search('USD (\d{1,4}).00', price).group(1)

    def product_id(self, selector):
        return selector.css(
            'h3 span[itemprop="productID"]::text').extract_first()

    def image_paths(self, selector):
        return selector.css(
            'div[class="product-images"]::attr(data-images)').extract_first()

    def product_quantity(self, selector):
        return selector.css(
            'select[id="Quantity"]::attr(value)').extract_first()
