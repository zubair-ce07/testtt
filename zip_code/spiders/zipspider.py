import urlparse
from scrapy.spider import Spider
from zip_code.items import ZipCodeItem
from scrapy.http import Request

class ZipSpider(Spider):
    name = 'zipSpider'
    allowed_domains = ['zip-codes.com']

    def start_requests(self):
        with open('missing_zips.txt', 'r') as file:
            for line in file:
                code = line.strip()
                url = 'http://www.zip-codes.com/zip-code/'+code+'/zip-code-'+code+'.asp'
                yield self.make_requests_from_url(url)


    # Scrap data from given zip code url
    def parse(self,response):
        zip_detail = ZipCodeItem()
        zip_detail['state'] = response.xpath(
            '//td[a[contains(text(),"State:")]]/following-sibling::td//text()'
            ).extract()[0]
        cities = response.xpath(
            '//td[a[contains(text(),"City")]]/following-sibling::td//a')
        counties = response.xpath(
            '//td[a[contains(text(),"Counties")]]/following-sibling::td//a')
        if cities:
            c = cities.pop(0)
            yield Request(
                urlparse.urljoin(response.url, c.xpath('./@href').extract()[0]),
                meta = {'cities': cities, 'item': zip_detail, 'counties' : counties,
                    'total_city_population' : 0 , 'total_county_population' : 0,
                    'city_name': c.xpath('./text()').extract()[0]},
                callback=self.parse_city_population, dont_filter=True
                )


    # Compare Counties Population
    def parse_county_population(self, response):
        zip_detail=response.meta.get('item')
        population = response.xpath(
            '//td[contains(text(),"Total population")]/following-sibling::td//text()'
            ).extract()[0]
        total_county_population = response.meta.get('total_county_population')
        if population > total_county_population:
            zip_detail['county'] = response.meta.get('county_name')
            total_county_population = population
        counties=response.meta.get('counties')
        if counties:
            c = counties.pop(0)
            yield Request(
                urlparse.urljoin(response.url, c.xpath('./@href').extract()[0]),
                meta = {'counties': counties, 'item': zip_detail,
                        'total_county_population' : total_county_population,
                        'county_name': c.xpath('./text()').extract()[0]},
                callback=self.parse_county_population
                )
            return
        yield zip_detail


    # Compare Cities population
    def parse_city_population(self, response):
        zip_detail=response.meta.get('item')
        population = response.xpath(
            '//td[contains(text(),"Total population")]/following-sibling::td//text()'
            ).extract()[0]
        total_city_population = response.meta.get('total_city_population')
        if population > total_city_population:
            zip_detail['city'] = response.meta.get('city_name')
            total_city_population = population
        counties=response.meta.get('counties')
        cities=response.meta.get('cities')
        if cities:
            c = cities.pop(0)
            yield Request(
                urlparse.urljoin(response.url, c.xpath('./@href').extract()[0]),
                meta = {'cities': cities, 'item': zip_detail, 'counties' : counties,
                        'total_city_population' : total_city_population,
                        'total_county_population' : 0,
                        'city_name': c.xpath('./text()').extract()[0]},
                callback=self.parse_city_population
                )                                               # Get Next city request
            return
        elif counties:
            c = counties.pop(0)
            yield Request(
                urlparse.urljoin(response.url, c.xpath('./@href').extract()[0]),
                meta = {"counties": counties, 'item': zip_detail,
                        'total_county_population' : 0,
                        'county_name': c.xpath('./text()').extract()[0]},
                callback=self.parse_county_population, dont_filter=True
                )                                               # Get Next County request
            return

