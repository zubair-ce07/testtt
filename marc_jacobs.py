#!/usr/bin/env python3
import json
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Product:
    def __init__(self,
                 product_name,
                 product_category,
                 source_url
                 ):
        self.product_name = product_name
        self.product_category = product_category
        self.source_url = source_url
        self.images = []
        self.skus = []

    def addImages(self, image):
        self.images.append(image)

    def append(self, sku):
        self.skus.append(
            {
                'color': sku.product_color,
                'size': sku.product_size,
                'price': sku.product_price,
                'availability': sku.availability
            }
        )


class Sku:
    def __init__(self,
                 product_color,
                 product_price,
                 product_size,
                 availability):
        self.product_color = product_color
        self.product_price = product_price
        self.product_size = product_size
        self.availability = availability


class MarcJacobsSpider(CrawlSpider):
    name = "marcjacobs_spider"

    start_urls = ['https://www.marcjacobs.com/']

    rules = (
        Rule(LinkExtractor(restrict_css=[
                'li.mobile-hidden div.level-2 ul.level-3 a']),
             callback='parse_major_category'),
        Rule(LinkExtractor(restrict_css=[
                'li.mobile-hidden div.level-2 ul.menu-vertical a']),
             callback='parse_major_category'),
        Rule(LinkExtractor(restrict_css=[
                'li.mobile-hidden:first-of-type a']),
             callback='parse_major_category'),
        )

    def product_format(self, product):
        return {
            'name': product.product_name,
            'category': product.product_category,
            'source_url': product.source_url,
            'images': product.images,
            'skus': product.skus
        }

    def get_product_category(self, response):
        return response.css('a.breadcrumb-element::text').extract()

    def parse_major_category(self, response):

        category = self.get_product_category(response)

        links_to_product_pages = response.css(
            'a.product-page-link::attr(href)').extract_first()

        yield response.follow(links_to_product_pages,
                              self.parse_product_page,
                              meta={'category': category})

    def get_color_urls(self, response):
        return response.css(
            'a.swatchanchor::attr(href)').extract()

    def get_color_name(self, response):
        return response.css(
            'a.swatchanchor::text').extract()

    def get_color_with_urls(self, response):
        product_colors_urls = self.get_color_urls(response)
        product_colors_names = self.get_color_name(response)

        return{

                'remaining_color_urls': product_colors_urls,
                'remaining_color_names': product_colors_names,

              }

    def get_product_name(self, response):
        return response.css(
            'h1.product-name::text').extract_first()

    def parse_product_page(self, response):
        product_name = self.get_product_name(response)

        product_category = response.meta['category']

        remaining_colors_elements = self\
            .get_color_with_urls(
                response)

        top_color_url, top_color_name = self.get_next_color_and_its_link(
            remaining_colors_elements)

        single_product = Product(product_name, product_category, response.url)

        yield response.follow(top_color_url + '&Quantity=1&format=ajax',
                              self.parse_color_of_product_page,
                              meta={
                                  'product': single_product,
                                  'top_color_name': top_color_name,
                                  'remaining_colors_elements':
                                              remaining_colors_elements,
                                  'image_sources': [],
                              })

    def parse_images(self, response):
        images = json.loads(response.text[26:-2])

        for item in images['items']:
            response.meta['product'].addImages(item['src'])

        if response.meta['path_to_images']:
            path_to_next_image = response.meta['path_to_images'].pop(0)
            yield response.follow(
                path_to_next_image,
                self.parse_images,
                meta={
                    'product': response.meta['product'],
                    'path_to_images': response.meta['path_to_images']
                })

        else:
            yield self.product_format(response.meta['product'])

    def get_size_options(self, response):
        options = response.css(
            'select#va-size option[value!=""]::text').extract()
        return list(map(str.strip, options))

    def get_size_urls(self, response):
        return response.css(
            'select[id="va-size"] option[value!=""] ::attr(value)').extract()

    def get_available_sizes_and_urls(self, response):

        color_size_options = self.get_size_options(response)

        color_size_product_urls = self.get_size_urls(response)

        return{

                'color_size_options': color_size_options,
                'color_size_product_urls': color_size_product_urls

              }

    def parse_color_of_product_page(self, response):
        size_elements_of_this_color = self\
            .get_available_sizes_and_urls(
                response)

        next_color_size, next_size_url = self.get_next_size_and_its_link(
            size_elements_of_this_color)

        path_to_images = response.css(
            'div[class="product-images"]::attr(data-images)').extract_first()

        response.meta['image_sources'].append(path_to_images)

        yield response.follow(next_size_url + '&Quantity=1&format=ajax',
                              self.parse_color_size_product_page,
                              meta={
                                    'size': next_color_size,
                                    'size_elements_of_this_color':
                                              size_elements_of_this_color,
                                    'product': response.meta['product'],
                                    'top_color_name':
                                              response.meta['top_color_name'],
                                    'remaining_colors_elements':
                                              response.meta[
                                                  'remaining_colors_elements'],

                                    'image_sources': response.meta[
                                        'image_sources']

                              }, )

    def get_next_size_and_its_link(self, size_elements_of_this_color):

        next_size = size_elements_of_this_color['color_size_options'].pop(0)
        next_size_page_link = size_elements_of_this_color[
                                'color_size_product_urls'].pop(0)
        return next_size, next_size_page_link

    def get_next_color_and_its_link(self, remaining_color_elements):
        if remaining_color_elements['remaining_color_urls']:

            next_color_url = remaining_color_elements[
                                'remaining_color_urls'].pop(0)
            next_color_name = remaining_color_elements[
                                'remaining_color_names'].pop(0)

            return next_color_url, next_color_name

        else:
            return None

    def get_sku(self, response):
        size_color = response.meta['top_color_name']

        quantity_of_product = response.css(
            'select[id="Quantity"]::attr(value)').extract_first()

        availability = False
        if quantity_of_product:
            availability = True

        price_of_size = response.css(
            'span[itemprop="price"]::attr(content)').extract_first()
        price_of_size = str(int(price_of_size[4:-3]))

        return Sku(size_color,
                   price_of_size,
                   response.meta['size'],
                   availability)

    def parse_color_size_product_page(self, response):

        size_color_sku = self.get_sku(response)
        response.meta['product'].append(size_color_sku)

        remaining_colors_elements = response.meta[
            'remaining_colors_elements']
        size_elements_of_this_color = response.meta[
            'size_elements_of_this_color']

        if size_elements_of_this_color['color_size_product_urls']:

            next_size, next_size_url = self.get_next_size_and_its_link(
                                            size_elements_of_this_color)

            yield response.follow(
                next_size_url + '&Quantity=1&format=ajax',
                self.parse_color_size_product_page,
                meta={
                      'size': next_size,
                      'size_elements_of_this_color':
                                size_elements_of_this_color,
                      'product': response.meta['product'],
                      'top_color_name':
                                response.meta['top_color_name'],
                      'remaining_colors_elements':
                                response.meta['remaining_colors_elements'],

                      'image_sources': response.meta[
                                        'image_sources']
                    })

        elif remaining_colors_elements['remaining_color_urls']:

            next_color_url, next_color_name = self.get_next_color_and_its_link(
                                                remaining_colors_elements)

            yield response.follow(next_color_url + '&Quantity=1&format=ajax',
                                  self.parse_color_of_product_page,
                                  meta={
                                      'top_color_name': next_color_name,
                                      'image_sources': response.meta[
                                              'image_sources'],
                                      'product': response.meta['product'],

                                      'remaining_colors_elements':
                                          remaining_colors_elements
                                  })
        else:

            path_to_images = response.meta['image_sources'].pop(0)
            yield response.follow(path_to_images, self.parse_images, meta={
                'product': response.meta['product'],
                'path_to_images': response.meta['image_sources']
            })
