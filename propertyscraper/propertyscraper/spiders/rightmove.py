import re
import scrapy
from dateutil import parser
import datetime
import itertools

from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from propertyscraper.items import PropertyscraperItem


def make_urls(start_urls_temp, sort_types):
    return [u.format(s) for u in start_urls_temp for s in sort_types]


class Mixin:
    name = "rightmove"
    allowed_domains = ['rightmove.co.uk']
    start_urls_temp = [('https://www.rightmove.co.uk/student-accommodation/find.html?locationIdentifier=REGION%5E87490'
                        '&insId=1&radius=40.0&sortType={}'),
                       ('https://www.rightmove.co.uk/student-accommodation/find.html?locationIdentifier=REGION%5E87490'
                        '&radius=40.0&propertyTypes=detached&secondaryDisplayPropertyType=detachedshouses&sortType={}'),
                       ('https://www.rightmove.co.uk/student-accommodation/find.html?locationIdentifier=REGION%5E87490'
                        '&radius=40.0&propertyTypes=semi-detached&secondaryDisplayPropertyType=semidetachedhouses'
                        '&sortType={}'),
                       ('https://www.rightmove.co.uk/student-accommodation/find.html?locationIdentifier=REGION%5E87490'
                        '&radius=40.0&propertyTypes=terraced&secondaryDisplayPropertyType=terracedhouses&sortType={}'),
                       ('https://www.rightmove.co.uk/student-accommodation/find.html?locationIdentifier=REGION%5E87490'
                        '&radius=40.0&propertyTypes=flat&primaryDisplayPropertyType=flats&sortType={}'),
                       ('https://www.rightmove.co.uk/student-accommodation/find.html?locationIdentifier=REGION%5E87490'
                        '&radius=40.0&propertyTypes=bungalow&primaryDisplayPropertyType=bungalows&sortType={}'),
                       ('https://www.rightmove.co.uk/student-accommodation/find.html?locationIdentifier=REGION%5E87490'
                        '&radius=40.0&propertyTypes=private-halls&sortType={}'),
                       ]

    sort_types = ['1', '2', '10', '']
    start_urls = make_urls(start_urls_temp, sort_types)


class RightmoveParseSpider(Spider, Mixin):
    name = f"{Mixin.name}-parse"

    amenities = ['friendly', 'pets', 'smoking', 'storage', 'spacious', 'window', 'sun']
    property_types = ['Studio', 'Flat', 'House', 'Apartment', 'Maisonette', 'Room', 'Hall']
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov',
              'Dec']

    def parse(self, response):
        property_item = PropertyscraperItem()

        property_item['property_name'] = self.property_name(response)
        property_item['street_address_1'] = self.street_address(response)
        property_item['street_address_2'] = ''
        property_item['city'] = 'London'
        property_item['postcode'] = self.postcode(response)
        property_item['area'] = self.area(response)
        property_item['area_info'] = ''
        property_item['website'] = self.website(response)
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
        property_item['property_contact_email'] = self.property_contact_email(response)
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

    def property_contact_email(self, response):
        description = self.description(response)
        contact_email = [''.join(re.findall('[a-zA-Z-0-9_]+@[a-z]+.[a-z]{3,5}', d)) for d in description if
                         ''.join(re.findall('[a-zA-Z-0-9_]+@[a-z]+.[a-z]{3,5}', d))]
        return contact_email[0] if contact_email else ''

    def postcode(self, response):
        page = response.xpath(
            '//script[contains(text(), "RIGHTMOVE.ANALYTICS.DataLayer.pushKV")]/text()').extract_first()
        for s in page.split(','):
            if 'post' in s:
                return s.split('"')[-2]

    def website(self, response):
        website_x = '//div[@class="agent-details-display"]/p[contains(@class, "overflow-hidden")]/a/@href'
        return response.xpath(website_x).extract()

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
        letting_info.extend(self.property_amenities(response))
        letting_info.extend(self.combine_description_and_amenities(response))

        move_in_info = [r for r in letting_info if 'available' in r.lower()]

        if move_in_info:
            try:
                move_in_date_info = move_in_info[0].split(':')[1]
                date = parser.parse(move_in_date_info)
                return date.strftime("%d/%m/%Y")
            except ValueError:
                if 'Now' in move_in_date_info:
                    return datetime.datetime.now().strftime("%d/%m/%Y")
            except IndexError:
                date = re.findall('(?:on|from|:)\s*([a-zA-Z0-9,\s]{1,17}20[\d]{2})', move_in_info[0])
                try:
                    date = parser.parse(date[0])
                    return date.strftime("%d/%m/%Y")
                except IndexError:
                    if re.findall('immediately|now', ''.join(move_in_info[0]).lower()):
                        return datetime.datetime.now().strftime("%d/%m/%Y")
                    if re.findall('mid|end|beginning', ''.join(move_in_info[0]).lower()):
                        month = re.findall('(?:mid|end|beginning)\s*([a-zA-Z0-9]+)', move_in_info[0])
                        month = parser.parse(month[0])
                        return month.strftime("%d/%m/%Y")
                    month = [m for m in self.months if m in move_in_info[0]]
                    if month:
                        regex_mm_yy = '{0}\s20[\d]{{2}}'.format(month[0])
                        regex_ddth_mm_yy = '[\d]{{2}}th\s{0}\s20[\d]{{2}}'.format(month[0])
                        regex_dd_mm_yy = '[\d]{{2}}\s{0}\s20[\d]{{2}}'.format(month[0])
                        date = re.findall(regex_dd_mm_yy, move_in_info[0]) \
                               or re.findall(regex_ddth_mm_yy, move_in_info[0]) \
                               or re.findall(regex_mm_yy, move_in_info[0])
                        date = parser.parse(date[0])
                        return date.strftime("%d/%m/%Y")

    def deposit_amount(self, response):
        property_info = self.combine_description_and_amenities(response)
        deposit_info = [l for l in property_info if 'deposit' in l.lower()]
        if deposit_info:
            try:
                return deposit_info[0].split(':')[1] if deposit_info else ''
            except IndexError:
                regex = '(?:deposit.*?)(?:(£[\d,]+|\s[\d,]+\spounds)|(?:agency|agent|fee))'
                deposit_amount = [' '.join(list(re.findall(regex, d.lower()))) for d in deposit_info if
                                  ' '.join(list(re.findall(regex, d.lower())))]
                if deposit_amount:
                    return deposit_amount[0]
        return ''

    def deposit_name(self, response):
        property_info = self.combine_description_and_amenities(response)
        deposit_name = ""
        deposit_info = [l for l in property_info if 'deposit' in l.lower()]
        if deposit_info:
            regex = 'Deposit|Bond|Security|Holding'
            deposit_name = [' '.join(re.findall(regex, d)) for d in deposit_info if
                            re.findall(regex, d) and re.findall('£|pounds', d)]
        return deposit_name[0] if deposit_name else ''

    def combine_description_and_amenities(self, response):
        property_info = self.letting_info(response)
        property_info.extend(self.description(response))
        property_info.extend(self.property_amenities(response))
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
        floor_plan_css = '#floorplan img.site-plan::attr(src)'
        floor_plan_css_alt = '#floorplan .zoomableimagewrapper img::attr(src)'
        floor_plan_image = response.css(floor_plan_css).extract_first() or response.css(
            floor_plan_css_alt).extract_first()
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
        property_info = self.combine_description_and_amenities(response)
        property_info.append(self.property_name(response))
        room_name = ""

        bedroom_count = [''.join(re.findall('[\d]+\sbedroom', i.lower())) for i in property_info if
                         ''.join(re.findall('[\d]+\sbedroom', i.lower()))]
        if bedroom_count:
            print(bedroom_count)
            room_name = bedroom_count[0]

        bathroom_count = [''.join(re.findall('[\d]+\sbathroom', i.lower())) for i in property_info if
                          ''.join(re.findall('[\d]+\sbathroom', i.lower()))]
        if bathroom_count:
            room_name = f"{room_name}, {bathroom_count[0]}"

        reception_room_count = [''.join(re.findall('[\d]+\sreception\sroom', i.lower())) for i in property_info if
                                ''.join(re.findall('[\d]+\sreception\sroom', i.lower()))]

        if reception_room_count:
            room_name = f"{room_name}, {reception_room_count[0]}"

        return room_name

    def raw_images(self, response):
        images = response.css('.gallery-thumbs-list li meta::attr(content)').extract()
        larger_image_regex = '(.*)(?:_max[\d_x]+)(.[a-z]+)'
        images = [''.join(list(re.findall(larger_image_regex, image)[0])) for image in images]
        return images

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
    sumtotal = 0

    name = f"{Mixin.name}-crawl"
    property_url = '//a[contains(@class, "propertyCard-img-link")]'
    rules = [Rule(LinkExtractor(restrict_xpaths=property_url), callback=parser.parse)]

    def parse(self, response):
        for request in super(RightmoveCrawlSpider, self).parse(response):
            yield request

        requests = []
        if 'minPrice' not in response.url:
            # price filters request
            requests = self.generate_price_filter_requests(response)
        elif 'index' not in response.url:
            requests = self.generate_pagination_requests(response)

        for request in requests:
            yield request

    def generate_pagination_requests(self, response):
        requests = []
        total = response.css('.searchHeader-resultCount ::text').extract_first()
        total = int(total.replace(",", ""))

        for index in range(1, int(total / 24)):
            next_url = f"{response.url}&index={int(index)*24}"
            requests.append(scrapy.Request(url=next_url, callback=self.parse))

        return requests

    def generate_price_filter_requests(self, response):
        requests = []
        bedding_range = response.css('#bedroomFilterBar select[name="minBedrooms"] option ::attr(value)').extract()
        bedding_range = [r for r in bedding_range if r]
        bedding_range_chunks = list(zip(*[iter(bedding_range)] * 2))

        price_range = response.css('#priceFilterBar select[name="minPrice"] option ::attr(value)').extract()
        price_range = [r for r in price_range if r]
        price_range_chunks = list(zip(*[iter(price_range)] * 6))

        for pair in list(itertools.product(bedding_range_chunks, price_range_chunks)):
            next_chunk = (f"{response.url}&maxPrice={pair[1][-1]}&minPrice={pair[1][0]}&"
                          f"maxBedrooms={pair[0][1]}&minBedrooms={pair[0][0]}")
            requests.append(scrapy.Request(url=next_chunk, callback=self.parse))

        return requests
