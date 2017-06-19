import scrapy
import re
import json


class OrsaySpider(scrapy.Spider):
    name = 'orsay'
    #allowed_domains = ['http://www.orsay.com/de-de/collection.html']

    start_urls = [
        'http://www.orsay.com/de-de/collection.html',
        'http://www.orsay.com/de-de/accessoires.html']

    def parse(self, response):
        for site in response.xpath(
                "//ul[@class='product-colors product-item-color']//a/@href").extract():
            yield scrapy.Request(site, callback=self.parseprod)
        for href in response.xpath("//a[@class='next i-next']/@href"):
            yield response.follow(href, self.parse)

    def parseprod(self, response):
        data_file = open('orsay.json', 'a+')
        sizes_list = list(filter(None, [n.strip() for n in response.css(
            'div.sizebox-wrapper li::text ').extract()]))
        avail_list = response.xpath(
            "//div[@class='sizebox-wrapper']//li/@data-qty").extract()
        data = {
            'url': "",
            'brand': "",
            'care': "",
            'description': "",
            'image_urls': "",
            'name': "",
            'retailer_sku': "",
            'urls-color': "",
            'skus': []
        }
        data['url'] = response.url
        data['brand'] = response.xpath(
            "//script[@type='application/ld+json']/text()").re(r'Brand.*name":"(\w*)"},')[0]
        data['care'] = response.xpath(
            "//div[@class='product-care six columns']//@src"
            + " | //p[@class='material']/text()").extract()
        data['description'] = str(response.xpath(
            "//p[@class='description']/text()").extract()[0]).strip()
        data['image_urls'] = response.xpath(
            "//div[@class='product-image-gallery-thumbs configurable']//@href").extract()
        data['name'] = response.css("h1.product-name::text").extract()
        data['url-colors'] = [n.strip() for n in response.xpath(
            "//ul[@class='product-colors']//a/@href").extract() if n != '#']
        data['retailer_sku'] = list(filter(None, response.css(
            "p.sku::text").re(r'(\d*)')))[0]
        for sizes in range(len(sizes_list)):
            if int(avail_list[sizes]):
                data['skus'].append({str(list(filter(None, response.css(
                    "p.sku::text").re(r'(\d*)')))[0] + '_' + sizes[sizes_list]):
                    {'color': response.css("img.has-tip[title]::attr(title)").extract()[0],
                     'currency': response.xpath(
                        "//script[@type='application/ld+json']/text()").re(r'priceCurrency\":\"(\w*)')[0], 'price': response.xpath(
                        "//script[@type='application/ld+json']/text()").re(r'price":(\d*\.\d*)')[0], 'size': sizes[sizes_list]}})
            else:
                data['skus'].append({str(list(filter(None, response.css(
                    "p.sku::text").re(r'(\d*)')))[0] + '_' + sizes[sizes_list]):
                    {'color': response.css("img.has-tip[title]::attr(title)").extract()[0],
                     'currency': response.xpath(
                        "//script[@type='application/ld+json']/text()").re(r'priceCurrency\":\"(\w*)')[0], 'price': response.xpath(
                        "//script[@type='application/ld+json']/text()").re(r'price":(\d*\.\d*)')[0], 'size': sizes[sizes_list], 'out_of_stock': 'true'}})

        json.dump(data, data_file)
        data_file.close()
