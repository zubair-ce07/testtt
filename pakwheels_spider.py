import scrapy
import mysql.connector as mc
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
            yield response.follow(url, self.parseCarsUrls)
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

        self.total += 1
        print('^'*50, self.total)
        self.dataToMysql(items['make'], items['model'], items['year'], items['millage'], items['transmission'],
                         items['engine_type'], items['reg_city'], items['assembly'], items['engine_capacity'],
                         items['body_type'], items['features'], items['description'])

        # print('^'*40, items['reg_city'])
        yield items

    def dataToMysql(self, make, model, year, millage, transmission, eng_type, reg_city, asmb, eng_cap
                    , body_type, features, desc):
        conn = mc.connect(user='root', password='1234', host='127.0.0.1')
        mycursor = conn.cursor()
        mycursor.execute('CREATE DATABASE IF NOT EXISTS wheelsDB')
        mycursor.execute('USE wheelsDB')

        tbl_des = (
            'CREATE TABLE IF NOT EXISTS usedCars('
            'used_cars_id int AUTO_INCREMENT,'
            'make varchar(15),'
            'model varchar(15),'
            'year varchar(5),'
            'millage varchar(10),'
            'transmission varchar(10),'
            'engine_type varchar(10),'
            'reg_city varchar(10),'
            'assembly varchar(10),'
            'engine_capacity varchar(10),'
            'body_type varchar(10),'
            'features varchar(500),'
            'description varchar(500),'
            'PRIMARY KEY(used_cars_id) )'
        )
        tbl_in_sql = """INSERT INTO usedCars(make, model, year, millage, transmission, engine_type, reg_city,
        assembly, engine_capacity, body_type, features, description)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        features = ''.join(i for i in features)
        features = features.strip()
        tbl_in_val = (make, model, year, millage, transmission, eng_type, reg_city, asmb,
                      eng_cap, body_type, features, desc)

        mycursor.execute(tbl_des)
        mycursor.execute(tbl_in_sql, tbl_in_val)

        conn.commit()
        mycursor.close()
        conn.close()
