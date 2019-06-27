import scrapy


class MySpider(scrapy.Spider):

    name = 'testify'
    start_urls = ['https://www.derek-rose.com/men/clothing.html?limit=all']

    def start_requests(self):

        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse)

    def parse(self, response):
        Links = response.css('.products-list__link::attr(href)').extract()
        for link in Links:
            absolute_url = link
            yield scrapy.Request(absolute_url, callback=self.mymain)

    def mymain(self, response):

        yield from self.desc(response)
        yield from self.links(response)
        yield from self.details(response)

    def links(self, response):

        mydixt = []

        for i in response.css('.media-extra__item'):

            p = i.css('.media-extra__item img::attr(srcset)').get().split()[18]
            mydixt.append(p)

        yield {'images_urls': mydixt}

    def details(self, response):

        description = {}
        properties = response.css('.product-details__attrs tr th::text').getall()
        values = response.css('.product-details__attrs tr td::text').getall()
        for index in range(0, len(properties) - 1):
            description[properties[index]] = values[index]

        yield {'Details and care': description}

    def desc(self, response):
        d = response.css('span.price::text').get()
        d = d[1:]
        d = float(d) * 100

        yield {

        'name': response.css('h1.product-details__sub::text').get(),
        'sub name': response.css('h2.product-details__obj::text').get(),
        'price in £': d,
        'Description': response.css(
            'div.product-details__main-description p::text').getall(),
        'Skus': response.css('.product-details__sku::text').getall(),
        }
























