import re
import scrapy
from dateutil import parser
import datetime

from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from propertyscraper.items import PropertyscraperItem


class Mixin:
    name = "rightmove"
    allowed_domains = ['rightmove.co.uk']
    start_urls = [('http://www.rightmove.co.uk/student-accommodation/find.html?locationIdentifier=REGION%5E87490'
                   '&insId=1&radius=40.0')]


class RightmoveParseSpider(Spider, Mixin):
    name = f"{Mixin.name}-parse"

    amenities = ['friendly', 'pets', 'smoking', 'storage', 'spacious', 'window', 'sun']
    property_types = ['Studio', 'Flat', 'House', 'Apartment', 'Maisonette', 'Room']

    def parse(self, response):
        property_item = PropertyscraperItem()

        property_item['property_name'] = self.property_name(response)
        property_item['street_address_1'] = self.street_address(response)
        property_item['street_address_2'] = ''
        property_item['city'] = ''
        property_item['postcode'] = ''
        property_item['area'] = self.area(response)
        property_item['area_info'] = ''
        property_item['website'] = ''
        property_item['furnished'] = self.furnished_info(response)
        property_item['bills_included'] = self.bills_included(response)
        property_item['property_type'] = self.property_type(response)
        property_item['move_in_date'] = self.move_in_date(response)
        property_item['move_out_date'] = ''
        property_item['deposit_amount'] = self.deposit_amount(response)
        property_item['property_amenities'] = ';'.join(self.property_amenities(response))
        property_item['property_images'] = self.property_images(response)
        property_item['property_description'] = self.description(response)
        property_item['room_images'] = self.room_images(response)
        property_item['room_name'] = self.room_name(response)
        property_item['room_availability'] = ''
        property_item['property_contact_name'] = ''
        property_item['property_contact_email'] = ''
        property_item['property_contact_number'] = self.property_contact_number(response)
        property_item['discounts'] = ''
        property_item['room_price'] = self.room_price(response)
        property_item['floor_plans'] = self.floorplan(response)
        property_item['deposit_name'] = self.deposit_name(response)
        property_item['deposit_type'] = ''
        property_item['room_amenities'] = ';'.join(self.room_amenities(response))
        property_item['property_ad_link'] = response.url
        property_item['agent_fees'] = self.agent_fees(response)
        property_item['agent_fees_amount'] = ''
        property_item['agent_name'] = self.agent_name(response)

        yield property_item

    def property_contact_number(self, response):
        contact_number_css = '.request-property-details strong::text'
        return response.css(contact_number_css).extract_first()

    def agent_name(self, response):
        return response.css('#aboutBranchLink strong ::text').extract_first()

    def letting_info(self, response):
        rows = response.css('#lettingInformation tr')
        letting_info = []
        for row in rows:
            letting_info.append(' '.join(row.css('td::text').extract()))

        return letting_info

    def furnished_info(self, response):
        letting_info = self.letting_info(response)
        furnished_info = [r for r in letting_info if 'furnish' in r.lower()]
        return furnished_info[0].split(':')[1] if furnished_info else ''

    def move_in_date(self, response):
        letting_info = self.letting_info(response)
        move_in_info = [r for r in letting_info if 'available' in r.lower()]
        move_in_date_info = ''
        if len(move_in_info) > 0:
            move_in_date_info = move_in_info[0].split(':')[1]
        try:
            date = parser.parse(move_in_date_info)
            return date.strftime("%d/%m/%Y")
        except ValueError:
            if 'Now' in move_in_date_info:
                return datetime.datetime.now().strftime("%d/%m/%Y")

    def deposit_amount(self, response):
        property_info = self.combine_description_and_amenities(response)
        deposit_info = [l for l in property_info if 'deposit' in l.lower()]
        try:
            return deposit_info[0].split(':')[1] if deposit_info else ''
        except IndexError:
            return ''

    def deposit_name(self, response):
        property_info = self.combine_description_and_amenities(response)
        deposit_info = [l for l in property_info if 'deposit' in l.lower()]
        return deposit_info[0].split(':')[0] if deposit_info else ''

    def combine_description_and_amenities(self, response):
        property_info = self.letting_info(response)
        property_info.extend(self.description(response))
        property_info.extend(self.property_amenities(response).split(';'))
        description = []
        for info in property_info:
            description.extend(info.split('.'))

        return description

    def agent_fees(self, response):
        description = self.combine_description_and_amenities(response)
        agent_fees_info = [d for d in description if 'agent fee' in d.lower()]
        raw_desc = ''.join(agent_fees_info)
        if not raw_desc:
            return ''
        return 'No' if 'No' in raw_desc else 'Yes'

    def room_amenities(self, response):
        descriptions = self.combine_description_and_amenities(response)
        amenities = [d for d in descriptions if any(a for a in self.amenities if a in d)]

        return amenities

    def floorplan(self, response):
        floor_plan_css = '#floorplan .zoomableimagewrapper img::attr(src)'
        floor_plan_image = response.css(floor_plan_css).extract_first()
        return floor_plan_image or 'Floorplan is not available'

    def room_price(self, response):
        price = response.css('.property-header-price strong::text').extract_first()
        return ''.join(re.findall('£|\d+', price))

    def area(self, response):
        street_address = self.street_address(response)
        return street_address.split(', ')[-1]

    def property_name(self, response):
        property_heading = response.css('.left h1::text').extract_first()
        return property_heading.split("to")[0]

    def room_name(self, response):
        property_heading = response.css('.left h1::text').extract_first()
        return property_heading.split("to")[0]

    def raw_images(self, response):
        return response.css('.gallery-thumbs-list li meta::attr(content)').extract()

    def property_images(self, response):
        images = self.raw_images(response)
        return images[:1] if images else ''

    def room_images(self, response):
        images = self.raw_images(response)
        return images[1:]

    def property_type(self, response):
        property_heading = response.css('.left h1::text').extract_first()
        property_type = [t for t in self.property_types if t.lower() in property_heading.lower()]
        if len(property_type) > 0:
            return property_type[0]

    def property_amenities(self, response):
        return response.css('.key-features li ::text').extract()

    def bills_included(self, response):
        description = self.combine_description_and_amenities(response)
        bills_info = [d for d in description if 'bills' in d.lower()]
        return bills_info[0] if bills_info else ''

    def street_address(self, response):
        return response.xpath('//meta[@itemprop="streetAddress"]/@content').extract_first()

    def description(self, response):
        raw_description = response.xpath('//p[@itemprop="description"]/text()').extract()
        return [self.clean_string(rd) for rd in raw_description if self.clean_string(rd)]

    def clean_string(self, target_str):
        return target_str.replace('\r', '').replace('\n', '').strip()


class RightmoveCrawlSpider(CrawlSpider, Mixin):
    parser = RightmoveParseSpider()

    name = f"{Mixin.name}-crawl"
    property_url = '//a[contains(@class, "propertyCard-img-link")]'
    rules = [Rule(LinkExtractor(restrict_xpaths=property_url), callback=parser.parse)]

    def parse(self, response):
        requests = super(RightmoveCrawlSpider, self).parse(response)
        for request in requests:
            yield request

        # price filters request
        if 'minPrice' not in response.url:
            range_list = response.css('#priceFilterBar select[name="minPrice"] option ::attr(value)').extract()

            range_list = [r for r in range_list if r]
            list_chunks = list(zip(*[iter(range_list)]*2))

            for i in list_chunks:
                next_chunk_url = f"{response.url}&maxPrice={i[-1]}&minPrice={i[0]}"
                yield scrapy.Request(url=next_chunk_url, callback=self.parse)

        # pagination links
        if 'index' not in response.url and 'minPrice' in response.url:
            total = response.css('.searchHeader-resultCount ::text').extract_first()
            total = int(total.replace(",", ""))

            for index in range(1, int(total/24)):
                next_url = f"{response.url}&index={int(index)*24}"
                yield scrapy.Request(url=next_url, callback=self.parse)
