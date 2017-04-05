import scrapy
from item import Product

class KithSpider(scrapy.Spider):
    name = "kithSpider"

    def start_requests(self):
        urls = ['https://kith.com/pages/women', 'https://kith.com/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        data = response.css('li.main-nav-list-item').css('ul')[3]

        for links in data.css('a::attr(href)').extract():
                yield scrapy.Request(response.urljoin(links), callback=self.parse_brand)

    def parse_brand(self, response):
        data = response.css('a.product-card-image-wrapper::attr(href)').extract()

        for links in data:
            yield scrapy.Request(response.urljoin(links), callback=self.parse_product)

    def parse_product(self, response):

        retailer_sku = response.css('input[id=product_id]::attr(value)').extract_first()
        brand_and_color = response.css('title::text').extract_first()
        brand_and_color = brand_and_color[:-14]
        brand_and_color = brand_and_color.split('-')
        brand = brand_and_color[0]

        if len(brand_and_color) >= 2:
            color = brand_and_color[1]
        else:
            color = "no Variant"

        price = response.css('span[id = ProductPrice]::text').extract_first()
        currency = response.xpath('//meta[@itemprop="priceCurrency"]/@content').extract_first()
        data = response.css('.product-single-details-rte')
        description = data.css('li::text').extract()
        description = description + data.css('p::text').extract()

        image_urls = response.css('img.js-super-slider-photo-img::attr(src)').extract()

        skus = {}

        for item in response.css('select[id=productSelect] > option'):
            temp_dict = {}
            size = item.css('option::text').extract_first().strip()
            size = size.split("-")
            if len(size) >= 2:
                sku = color.strip() + "_" + size[0].strip()
                out_of_stock = True
            else:
                sku = item.css('option::attr(data-sku)').extract_first()
                out_of_stock = False
            size = size[0]

            temp_dict.update({'color': color.strip().encode("utf-8"),
                              'currency': currency.strip().encode("utf-8"),
                              'price': price.strip().encode("utf-8"),
                              'size': size.strip().encode("utf-8"),
                              'out_of_stock': out_of_stock})

            skus[str(sku).strip().encode("utf-8")] = temp_dict

        product = Product(retailer_sku=retailer_sku, brand=brand, description=description, image_urls=image_urls, skus=skus)
        product = clean(product)

        return product


def clean(product):
    product['retailer_sku'] = product['retailer_sku'].strip().encode("utf-8")
    product['brand'] = product['brand'].strip().encode("utf-8")
    i = 0

    for de in product['description']:
        product['description'][i] = de.strip().encode("utf-8")
        i += 1

    return product
