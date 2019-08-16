import scrapy
from ..items import PakwheelsItem


class scrapySpider(scrapy.Spider):
    name = 'wheels'
    start_urls = [
        'http://pakwheels.com/'
    ]
    total = 0

    def parse(self, response):
        used_cars_url = response.css('a[title="Used Cars for sale in Pakistan"]::attr(href)').extract_first()
        yield response.follow(used_cars_url, self.parseUsedCarsUrl)

    def parseUsedCarsUrl(self, response):
        company_urls = response.css('li.heading > a::attr(href)').extract()
        for url in company_urls:
            yield response.follow(url, self.parseCompanyUrls)

    def parseCompanyUrls(self, response):
        cars_urls = response.css('.ad-detail-path::attr(href)').extract()
        for url in cars_urls:
            response.follow(url, self.parseCarsUrls)
        # nex_page_url = response.css('li.next_page > a::attr(href)').extract_first()
        # response.follow(nex_page_url, self.parseCompanyUrls)

    def getTrueValue(self, v1, v2):
        return next(i for i in [v1, v2] if i is not None)

    def parseCarsUrls(self, response):
        items = PakwheelsItem()
        items['make'] = response.xpath('//*[@id="main-container"]/div/div[1]/div[1]/div/ul/li[3]/a/span/text()').get()
        items['model'] = response.xpath('//*[@id="main-container"]/div/div[1]/div[1]/div/ul/li[4]/a/span/text()').get()
        items['year'] = self.getTrueValue(response.css('p[itemprop="vehicleModelDate"] > a::text').get(),
                                          response.css('p[itemprop="vehicleModelDate"]::text').get())
        items['year'] = items['year'].split()[0]
        items['millage'] = response.css('p[itemprop="mileageFromOdometer"]::text').get()
        items['transmission'] = self.getTrueValue(response.css('p[itemprop="vehicleTransmission"] > a::text').get(),
                                                  response.css('p[itemprop="vehicleTransmission"]::text').get())
        items['engine_type'] = self.getTrueValue(response.css('p[itemprop="fuelType"] > a::text').get(),
                                                 response.css('p[itemprop="fuelType"]::text').get())
        items['reg_city'] = response.css('#scroll_car_detail > li:nth-child(2)::text').get()
        items['assembly'] = self.getTrueValue(response.css('#scroll_car_detail > li:nth-child(6) > a::text').get(),
                                              response.css('#scroll_car_detail > li:nth-child(6)::text').get())
        items['engine_capacity'] = response.css('#scroll_car_detail > li:nth-child(8)::text').get()
        items['body_type'] = response.css('#scroll_car_detail > li:nth-child(10) > a::text').get()
        items['features'] = response.css('.car-feature-list > li::text').getall()
        var = response.css('div[itemprop="description"]::text').getall()
        var = ''.join(i for i in var)
        var = var.replace("\t", " ")
        var = var.replace("\r", "")
        items['description'] = var.strip()
        yield items
