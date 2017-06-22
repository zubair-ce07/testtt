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
             'a[title="NEW ARRIVALS"]']), follow=True),
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

    def parse_product_page(self, response):

        id = self.product_id(response)
        product_name = self.get_product_name(response)
        product_category = self.get_product_category(response)
        remaining_colors_elements = self.color_url_combinations(response)

        single_product = MarcJacobProduct(
            product_id=id,
            product_name=product_name,
            product_category=product_category,
            source_url=response.url,
            images=[],
            skus=[]
        )
        # print(colored(product_name, 'blue'))

        yield self.next_color_request(response, remaining_colors_elements,
                                      single_product)

    def next_color_request(self, response, remaining_color_elements, product,
                           source=[]):

        next_color_url, next_color_name = self.next_color_with_link(
            remaining_color_elements)
        yield response.follow(next_color_url + '&Quantity=1&format=ajax',
                              self.parse_color_of_product_page,
                              meta={
                                  'product': product,
                                  'next_color_name': next_color_name,
                                  'remaining_color_elements':
                                      remaining_color_elements,
                                  'image_sources': source,
                              })

    def parse_color_of_product_page(self, response):
        size_elements_of_this_color = self.size_url_combinations(response)

        path_to_images = self.image_paths(response)
        response.meta['image_sources'].append(path_to_images)
        yield self.next_size_request(response, size_elements_of_this_color)

    def next_size_request(self, response, remaining_size_urls):
        next_color_size, next_size_url = self.next_size_with_link(
            remaining_size_urls)
        yield response.follow(next_size_url + '&Quantity=1&format=ajax',
                              self.parse_color_size_product_page,
                              meta={
                                  'size': next_color_size,
                                  'size_elements_of_this_color':
                                              remaining_size_urls,
                                  'product': response.meta['product'],
                                  'next_color_name':
                                              response.meta['next_color_name'],
                                  'remaining_color_elements':
                                              response.meta[
                                                  'remaining_color_elements'],
                                  'image_sources': response.meta[
                                      'image_sources']

                              })

    def parse_color_size_product_page(self, response):

        size_color_sku = self.product_sku(response)
        response.meta['product'].append(size_color_sku)

        remaining_color_elements = response.meta[
            'remaining_color_elements']
        size_elements_of_this_color = response.meta[
            'size_elements_of_this_color']

        if size_elements_of_this_color:
            yield self.next_size_request(response, size_elements_of_this_color)
        elif remaining_color_elements:
            yield self.next_color_request(response, remaining_color_elements,
                                          response.meta['product'])
        else:
            yield self.next_image_request(response,
                                          response.meta['image_sources'],
                                          response.meta['product'])

    def next_image_request(self, response, image_sources, product):
        path_to_images = image_sources.pop(0)
        yield response.follow(path_to_images, self.parse_images, meta={
            'product': product,
            'path_to_images': image_sources
        })

    def parse_images(self, response):
        images = json.loads(response.text[26:-2])
        response.meta['product'].extend(x['src'] for x in images['items'])

        if response.meta['path_to_images']:
            yield self.next_image_request(response,
                                          response.meta['path_to_images'],
                                          response.meta['product'])
        else:
            yield response.meta['product']

    def get_product_category(self, response):
        return response.css('a.breadcrumb-element::text').extract()

    def get_product_name(self, response):
        return response.css(
            'h1.product-name::text').extract_first()

    def get_size_options(self, response):
        options = response.css(
            'select#va-size option[value!=""]::text').extract()
        return list(map(str.strip, options))

    def color_url_combinations(self, selector):
        comibnations = []
        for color_tag in selector.css(
                'a[class="swatchanchor"]'):
            color = color_tag.css('::attr(href)').extract_first()
            color_url = color_tag.css('::text').extract_first()
            comibnations.append({'color': color, 'color_url': color_url})
        return comibnations

    def size_url_combinations(self, selector):

        comibnations = []

        for size_tag in selector.css(
                'select[id="va-size"] option[value!=""]').extract():
            size = size_tag.css('.::text').extract()
            size_url = size_tag.css('.::attr(value)').extract()
            comibnations.append({'size': size, 'size_url': size_url})
        return comibnations

    def next_size_with_link(self, remaining_size_urls):
        if remaining_size_urls:
            next_size_url = remaining_size_urls.pop(0)
            return next_size_url['size_url'], next_size_url['size']
        return None

    def next_color_with_link(self, remaining_color_urls):
        if remaining_color_urls:
            next_color_url = remaining_color_urls.pop(0)
            return next_color_url['color_url'], next_color_url['color']
        return None

    def product_sku(self, response):
        size_color = response.meta['next_color_name']
        quantity_of_product = self.product_quantity(response)

        availability = True if quantity_of_product else False

        price_of_size = response.css(
            'span[itemprop="price"]::attr(content)').extract_first()

        price_of_size = str(int(re.search('USD (\d{1,4}).00')))

        return {
            'color': size_color,
            'price': price_of_size,
            'size': response.meta['size'],
            'availability': availability
        }

    def product_id(self, selector):
        id = selector.css(
            'h3 span[itemprop="productID"]::text').extract()
        return id

    def image_paths(self, selector):
        return selector.css(
            'div[class="product-images"]::attr(data-images)').extract_first()

    def product_quantity(self, selector):
        return selector.css(
            'select[id="Quantity"]::attr(value)').extract_first()
