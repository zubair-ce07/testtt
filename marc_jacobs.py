#!/usr/bin/env python3
import json
import scrapy


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


class MarcJacobsSpider(scrapy.Spider):
    name = "marcjacobs_spider"

    def start_requests(self):
        start_url = 'https://www.marcjacobs.com/'

        yield scrapy.Request(url=start_url, callback=self.parse)

    def parse(self, response):
        major_categories_page_links = response.xpath(
            '//li[@class="mobile-hidden"]/a/@href').extract()

        for url in major_categories_page_links:
            yield response.follow(url, self.parse_single_major_category_page)

    def product_format(self, product):
        return {
            'name': product.product_name,
            'category': product.product_category,
            'source_url': product.source_url,
            'images': product.images,
            'skus': product.skus
        }

    def parse_single_major_category_page(self, response):
        links_to_product_pages = response.xpath(
            '//a[@class="product-page-link"]/@href').extract()
        for product_link in links_to_product_pages:
            yield response.follow(product_link, self.parse_product_page)

    def get_color_names_and_urls_of_single_product(self, response):
        product_colors_urls = response.xpath(
            '//a[@class="swatchanchor"]//@href').extract()
        product_colors_names = response.xpath(
            '//a[@class="swatchanchor"]//text()').extract()

        top_color_url = product_colors_urls.pop(0)
        top_color_name = product_colors_names.pop(0)

        return{

                'remaining_color_urls': product_colors_urls,
                'remaining_color_names': product_colors_names,

              }, top_color_url, top_color_name

    def parse_product_page(self, response):
        product_name = response.xpath(
            '//h1[@class="product-name"]/text()').extract_first()
        product_category = response.xpath(
            '(//ul[@class="breadcrumb pdp"])/li[last()]/a/text()')\
            .extract_first()

        remaining_colors_elements, top_color_url, top_color_name = self\
            .get_color_names_and_urls_of_single_product(
                response)

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

    def get_available_sizes_and_urls(self, response):
        options = response.xpath(
            '//select[@id="va-size"]//option[@value!=""]//text()').extract()

        color_size_options = list(map(str.strip, options))

        color_size_product_urls = response.xpath(
            '//select[@id="va-size"]//option[@value!=""]//@value').extract()

        next_size_to_traverse = color_size_options.pop(0)
        next_size_url = color_size_product_urls.pop(0)
        return{

                'color_size_options': color_size_options,
                'color_size_product_urls': color_size_product_urls

              }, next_size_to_traverse, next_size_url

    def parse_color_of_product_page(self, response):
        size_elements_of_this_color, next_color_size, next_size_url = self\
            .get_available_sizes_and_urls(
                response)

        path_to_images = response.xpath(
            '//div[@class="product-images"]/@data-images').extract_first()

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
        return next_size_page_link, next_size

    def get_next_color_and_its_link(self, remaining_color_elements):
        if remaining_color_elements['remaining_color_urls']:

            next_color_url = remaining_color_elements[
                                'remaining_color_urls'].pop(0)
            next_color_name = remaining_color_elements[
                                'remaining_color_names'].pop(0)

            return next_color_url, next_color_name

        else:
            return None

    def parse_color_size_product_page(self, response):

        size_color = response.meta['top_color_name']

        quantity_of_product = response.xpath(
            '//select[@id="Quantity"]//@value').extract_first()

        availability = False
        if quantity_of_product:
            availability = True

        price_of_size = response.xpath(
            '//span[@itemprop="price"]/@content').extract_first()
        price_of_size = str(int(price_of_size[4:-3]))

        size_color_sku = Sku(size_color,
                             price_of_size,
                             response.meta['size'],
                             availability)

        response.meta['product'].append(size_color_sku)

        remaining_colors_elements = response.meta[
            'remaining_colors_elements']
        size_elements_of_this_color = response.meta[
                                                'size_elements_of_this_color']
        if size_elements_of_this_color['color_size_product_urls']:

            next_size_url, next_size = self.get_next_size_and_its_link(
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
