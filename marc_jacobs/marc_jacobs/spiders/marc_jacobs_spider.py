import json
import re

import scrapy

from marc_jacobs.items import MarcJacobsItem


class MarcJacobsSpider(scrapy.Spider):
    name = 'marc_jacobs'
    start_urls = [
        'https://www.marcjacobs.com/'
    ]

    def parse(self, response):
        categories_urls = response.xpath(
            '//nav[@id="navigation"]/ul/li[@class!="mobile-show"]/div/ul/li/a/@href').extract()
        for url in categories_urls:
            yield scrapy.Request(url, callback=self.parse_product_url)

    def parse_product_url(self, response):
        product_urls = response.meta.setdefault('product_urls', [])
        product_urls += response.xpath('//a[@class="product-page-link"]/@href').extract()
        scrolling_url = response.xpath(
            '//div[@class="infinite-scroll-placeholder"]/@data-grid-url').extract_first()
        if scrolling_url:
            request = scrapy.Request(scrolling_url, callback=self.parse_product_url,
                                     meta={'product_urls': product_urls})
            yield request
        else:
            for url in product_urls:
                yield scrapy.Request(response.urljoin(url), callback=self.parse_product_detail)

    def parse_product_detail(self, response):
        item = MarcJacobsItem()
        item['url'] = response.url
        item['name'] = response.xpath('//*[@id="name"]/@value').extract_first()
        item['brand'] = response.xpath('//*[@id="brand"]/@value').extract_first()
        description = response.xpath(
            '//ul[@class="tabs-menu mobile-show"]/li[1]/div/text()').extract()
        item['description'] = [desc.strip() for desc in description if desc.strip()]
        colours_wise_product = response.xpath(
            '//ul[@class="swatches Color"]/li/a/@href | //ul[@class="swatches Color"]/li/a/text()'
        ).extract()

        if colours_wise_product:
            return scrapy.Request(
                colours_wise_product[0], callback=self.parse_colour_wise_product,
                meta={'colour': colours_wise_product[1], 'item': item,
                      'colour_wise_product': colours_wise_product[2:]})

    def parse_colour_wise_product(self, response):
        item = response.meta.get('item')
        colour = response.meta.get('colour')
        colour_wise_product = response.meta.get('colour_wise_product')
        skus = response.meta.setdefault('skus', [])
        images_json_url = response.meta.setdefault('images_json_url', [])

        previous_price = response.xpath('//*[@id="product-content"]/div[1]/div/'
                                        'span[@class="price-standard"]/text()').extract_first()
        if not previous_price:
            previous_price = '-'
        price = response.xpath('//*[@id="product-content"]/div[1]/span/@content'). \
            extract_first().split()
        currency = price[0]
        price = price[1]
        sizes = response.xpath('//*[@id="va-size"]/option/text()').re('\d+')
        for size in sizes:
            skus.append({'sku_id': '{}_{}'.format(colour, size),
                         'colour': colour,
                         'size': size,
                         'previous_price': previous_price,
                         'price': price,
                         'currency': currency})
        json_url = response.xpath('//div[@class="product-images"]/@data-images').extract_first()
        images_json_url.append({'colour': colour, 'json_url': json_url})

        if colour_wise_product:
            return scrapy.Request(
                colour_wise_product[0], callback=self.parse_colour_wise_product,
                meta={'colour': colour_wise_product[1], 'images_json_url': images_json_url,
                      'colour_wise_product': colour_wise_product[2:], 'item': item, 'skus': skus})
        else:
            item['skus'] = skus
            image_json_url = images_json_url[0]
            if images_json_url:
                return scrapy.Request(
                    image_json_url.get('json_url'), callback=self.parse_image_links,
                    meta={'colour': image_json_url.get('colour'),
                          'item': item, 'images_json_url': images_json_url[1:]})

    def parse_image_links(self, response):
        colour = response.meta.get('colour')
        item = response.meta.get('item')
        images_json_url = response.meta.get('images_json_url')
        images_url = response.meta.setdefault('images_url', [])

        colour_wise_images_urls = []
        coloured_images_json_url = json.loads(re.search(r'{.*}', response.text).group(0))
        for json_url in coloured_images_json_url['items']:
            colour_wise_images_urls.append(json_url['src'])
        images_url.append({colour: colour_wise_images_urls})

        if images_json_url:
            json_url = images_json_url[0]
            return scrapy.Request(
                json_url.get('json_url'), callback=self.parse_image_links,
                meta={'colour': json_url.get('colour'), 'images_url': images_url,
                      'item': item, 'images_json_url': images_json_url[1:]})
        else:
            item['images_url'] = images_url
            return item
