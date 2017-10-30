import scrapy
import re


class OrseySpider(scrapy.Spider):
    # name of spider
    name = 'orsay'

    # list of allowed domains
    allowed_domains = ['orsay.com']
    # starting url
    start_urls = ['http://www.orsay.com/de-de']
    # location of csv file
    custom_settings = {'FEED_URI': 'tmp/orsay.json'}

    def parse(self, response):
        nav_urls = response.css('li.level1 > a::attr(href)').extract()

        for url in nav_urls:
            yield scrapy.Request(url=url, callback=self.parse_category_page)

    def parse_category_page(self, response):
        product_urls = response.css('.product-image-wrapper > a::attr(href)').extract()

        for url in product_urls:
            yield scrapy.Request(url=url, callback=self.parse_product_page)

    def parse_product_page(self, response):
        # Extract product information

        name = response.css('.product-name::text').extract_first().strip()

        # id = response.css('.sku::text').extract()
        id_url = re.search(".*(\d{8}).html", response.url)
        id = id_url.group(1)

        description = response.css('.description::text').extract_first().strip().split(sep='.')
        care = response.css('.material::text').extract()

        breadcrumbs = response.css('ul.breadcrumbs')
        category = breadcrumbs.css('a::text').extract()
        # div_gallery = response.css('div.product-image-gallery')
        # images = div_gallery.css('img::attr(src)').extract_first().strip()

        images = response.css('[data-zoom-id=mainZoom]::attr(href)').extract()

        price = response.css('.price::text').extract_first()

        ul = response.css('.sizebox-wrapper > ul')
        sizes = ul.css('li::text').extract()

        for index in range(len(sizes)):
            sizes[index] = sizes[index].strip()
        # availability = ul.css('li::attr(class)').extract()

        color_temp = response.css('.product-colors')
        # color_urls = color_temp.css('a::attr(href)').extract()
        colors = color_temp.css('img::attr(title)').extract()

        product = {}
        product['brand'] = 'Orsay'
        product['description'] = description
        product['url'] = response.url
        product['gender'] = 'girls'
        product['name'] = name
        product['category'] = category

        # skus
        product['price'] = price
        product['currency'] = 'EUR'
        product['sizes'] = sizes
        product['colors'] = colors
        # product['availability'] =

        product['image_urls'] = images
        product['care'] = care
        product['id'] = id
        yield product

        next_page_url = response.css('li.next > a::attr(href)')
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse_product_page)