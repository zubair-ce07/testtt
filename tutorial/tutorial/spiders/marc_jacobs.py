import scrapy
import json


class MarcSpider(scrapy.Spider):
    name = "marc"

    start_urls = [
        'http://marcjacobs.com/',
    ]

    def parse(self, response):
        new_arrivals = response.xpath(
            '//li[@class="mobile-hidden"]/a/@href').extract_first()
        for url in new_arrivals:
            yield response.follow(url, self.url_parse)

    def url_parse(self, response):
        product_pages = response.xpath(
            '//a[@class="product-page-link"]/@href').extract_first()
        for product in product_pages:
            yield response.follow(product, self.product_page_parse)

    def get_colors_elements(self, response):
        urls = response.xpath('//a[@class="swatchanchor"]//@href').extract()
        names = response.xpath('//a[@class="swatchanchor"]//text()').extract()

        elements = {
            'urls': urls,
            'color_names': names,
        }
        return elements

    def product_page_parse(self, response):
        name = response.xpath(
            '//h1[@class="product-name"]/text()').extract_first()
        category = response.xpath(
            '(//ul[@class="breadcrumb pdp"])/li[last()]/a/text()').extract_first()
        images = []
        skus = []
        colors_elements = self.get_colors_elements(response)
        url = colors_elements['urls'].pop(0)
        color_name = colors_elements['color_names'].pop(0)
        yield response.follow(url + '&Quantity=1&format=ajax',
                              self.color_of_product_page_parse,
                              meta={
                                  'color_name': color_name,
                                  'source_url': response.url,
                                  'product_name': name,
                                  'product_category': category,
                                  'images': images,
                                  'skus': skus,
                                  'colors_elements': colors_elements,
                                  'product_sku': None
                              })
        #     skus.extend(color_skus_and_images['skus_of_this_color'])
        #     images.extend(color_skus_and_images['images_of_this_color'])
        # yield{
        #     "name": name,
        #     "category": category,
        #     "source_url": response.url,
        #     "images": images,
        #     "skus": skus
        # }

    def images_parse(self, response):
        print("||||||||||||||||||||||||||||||||",
              response.url, "||||||||||||||||||||||||||||||||||||||||", sep=" ")
        images = json.loads(response.text[26:-2])
        item_list = []
        for item in images['items']:
            item_list.append(item['src'])
        product_sku = response.meta['product_sku']
        product_sku['images'].extend(item_list)
        if response.meta['path_to_images']:
            path_to_images = response.meta['path_to_images'].pop(0)
            yield response.follow(path_to_images, self.images_parse, meta={
                'product_sku': product_sku,
                'path_to_images': response.meta['path_to_images']
            })
        else:
            yield product_sku
        # name = response.meta['name']
        # category = response.meta['category']
        # source = response.meta['source']
        # yield {
        #     'name': name,
        #     'category': category,
        #     'source_url': source,
        #     'images': item-list
        #
        # }

    def get_size_elements(self, response):
        options = response.xpath(
            '//select[@id="va-size"]//option[@value!=""]//text()').extract()
        size_options = list(map(str.strip, options))
        urls = response.xpath(
            '//select[@id="va-size"]//option[@value!=""]//@value').extract()

        return {
            'size_options': size_options,
            'urls': urls
        }

    def color_of_product_page_parse(self, response):
        size_elements_of_this_color = self.get_size_elements(response)
        product_sku = response.meta['product_sku']
        # color = response.meta['color_name']
        path_to_images = response.xpath(
            '//div[@class="product-images"]/@data-images').extract_first()
        response.meta['images'].append(path_to_images)
        url = size_elements_of_this_color['urls'].pop(0)
        size = size_elements_of_this_color['size_options'].pop(0)
        yield response.follow(url + '&Quantity=1&format=ajax',
                              self.size_of_color_of_product_page_parse,
                              meta={
                                  'size': size,
                                  'size_elements_of_this_color': size_elements_of_this_color,
                                  'prev_meta': response.meta,
                                  'product_sku': product_sku
                              })
        # sku = {
        #     'color': color,
        #     "size": size_elements_of_this_color['size_options'][index],
        #     "price": price_availablitiy['price'],
        #     "availability": price_availablitiy['availability']
        # }
        # skus_of_this_color.append(sku)

        # return {'skus_of_this_color': skus_of_this_color, 'images_of_this_color': item_list}

    def size_of_color_of_product_page_parse(self, response):

        color = response.meta['prev_meta']['color_name']
        size = response.meta['size']

        quantity = response.xpath(
            '//select[@id="Quantity"]//@value').extract_first()
        availability = False
        if quantity:
            availability = True
        price = response.xpath(
            '//span[@itemprop="price"]/@content').extract_first()
        price = price[4:-3]
        price = int(price)
        price = str(price)
        size_color_sku = {
            'color': color,
            'size': size,
            'price': price,
            'availability': availability

        }
        if not response.meta['product_sku']:
            prev_meta = response.meta['prev_meta']

            response.meta['product_sku'] = {
                'name': prev_meta['product_name'],
                'category': prev_meta['product_category'],
                'source_url': prev_meta['source_url'],
                'skus': [],
                'images': []
            }
        response.meta['product_sku']['skus'].append(size_color_sku)
        # path_to_images = response.xpath(
        #     '//div[@class="product-images"]/@data-images').extract_first()
        # item_list = response.follow(path_to_images, self.images_parse)
        #
        colors_elements = response.meta['prev_meta']['colors_elements']
        size_elements_of_this_color = response.meta['size_elements_of_this_color']
        if size_elements_of_this_color['urls']:
            url = size_elements_of_this_color['urls'].pop(0)
            size = size_elements_of_this_color['size_options'].pop(0)
            yield response.follow(url + '&Quantity=1&format=ajax',
                                  self.size_of_color_of_product_page_parse,
                                  meta={
                                      'size': size,
                                      'size_elements_of_this_color': size_elements_of_this_color,
                                      'prev_meta': response.meta['prev_meta'],
                                      'product_sku': response.meta['product_sku']
                                  })
        elif colors_elements['urls']:
            url = colors_elements['urls'].pop(0)
            color_name = colors_elements['color_names'].pop(0)
            name = response.meta['prev_meta']['product_name']
            source_url = response.meta['prev_meta']['source_url']
            category = response.meta['prev_meta']['product_category']
            images = response.meta['prev_meta']['images']
            skus = response.meta['prev_meta']['skus']
            yield response.follow(url + '&Quantity=1&format=ajax',
                                  self.color_of_product_page_parse,
                                  meta={
                                      'product_sku': response.meta['product_sku'],
                                      'color_name': color_name,
                                      'source_url': source_url,
                                      'product_name': name,
                                      'product_category': category,
                                      'images': images,
                                      'skus': skus,
                                      'colors_elements': colors_elements
                                  })
        else:
            path_to_images = response.meta['prev_meta']['images'].pop(0)
            yield response.follow(path_to_images, self.images_parse, meta={
                'product_sku': response.meta['product_sku'],
                'path_to_images': response.meta['prev_meta']['images']
            })
