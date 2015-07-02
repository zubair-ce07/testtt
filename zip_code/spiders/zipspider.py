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
                url = 'http://www.zip-codes.com/zip-code/%s/zip-code-%s.asp'%(code,code)
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
        c = cities.pop(0)
        if len(cities) >= 1:
            yield Request(
                urlparse.urljoin(response.url, c.xpath('./@href').extract()[0]),
                meta = {'cities': cities, 'item': zip_detail,
                    'counties' : counties, 'total_cities' : [],
                    'city_name': c.xpath('./text()').extract()[0]},
                callback=self.parse_city_population, dont_filter=True
                )
        elif len(cities) == 0:
            zip_detail['city'] =  c.xpath('./text()').extract()[0]
            county = counties.pop(0)
            if len(counties) >= 1:
                yield Request(
                    urlparse.urljoin(response.url, county.xpath('./@href').extract()[0]),
                    meta = {"counties": counties, 'item': zip_detail, 'total_counties' :[],
                        'county_name': county.xpath('./text()').extract()[0]},
                    callback=self.parse_county_population, dont_filter=True
                    )
            elif len(counties) == 0:
                zip_detail['county'] = county.xpath('./text()').extract()[0]
                yield zip_detail


    # Get all counties with respective population
    def parse_county_population(self, response):
        zip_detail = response.meta.get('item')
        county = []
        county.append(response.xpath(
            '//td[contains(text(),"Total population")]/following-sibling::td//text()'
            ).extract()[0])
        county.append(response.meta.get('county_name'))
        total_counties = response.meta.get('total_counties')
        total_counties.append(county)
        counties=response.meta.get('counties')
        if counties:
            c = counties.pop(0)
            yield Request(
                urlparse.urljoin(response.url, c.xpath('./@href').extract()[0]),
                meta = {'counties': counties, 'item': zip_detail,
                        'total_counties' :total_counties,
                        'county_name': c.xpath('./text()').extract()[0]},
                callback=self.parse_county_population
                )
            return
        zip_detail['counties'] = total_counties
        yield zip_detail


    # Get all cities with respective population
    def parse_city_population(self, response):
        zip_detail = response.meta.get('item')
        city =  []
        city.append(response.xpath(
            '//td[contains(text(),"Total population")]/following-sibling::td//text()'
            ).extract()[0])
        city.append(response.meta.get('city_name'))
        total_cities = response.meta.get('total_cities')
        total_cities.append(city)
        counties = response.meta.get('counties')
        cities = response.meta.get('cities')
        if cities:
            c = cities.pop(0)
            yield Request(
                urlparse.urljoin(response.url, c.xpath('./@href').extract()[0]),
                meta = {'cities': cities, 'item': zip_detail,
                        'counties' : counties,
                        'total_cities' : total_cities,
                        'city_name': c.xpath('./text()').extract()[0]},
                callback=self.parse_city_population
                )                                               # Get Next city request
        elif counties:
            c = counties.pop(0)
            if len(counties) >= 1:
                yield Request(
                    urlparse.urljoin(response.url, c.xpath('./@href').extract()[0]),
                    meta = {"counties": counties, 'item': zip_detail,
                            'total_counties' : [],
                            'county_name': c.xpath('./text()').extract()[0]},
                    callback=self.parse_county_population, dont_filter=True
                    )                                               # Get Next County request
            elif len(counties) == 0:
                zip_detail['county'] =  c.xpath('./text()').extract()[0]
                zip_detail['cities'] = total_cities
                yield zip_detail


