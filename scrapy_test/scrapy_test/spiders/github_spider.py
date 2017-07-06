import scrapy


class GithubSpider(scrapy.Spider):
    name = 'github_spider'

    def start_requests(self):
        # creating url for profile with provided parameter in crawl command
        yield scrapy.Request('https://www.github.com/{username}'.format(username=self.username))

    def parse(self, response):
        # get h3 which contains the date of contributions
        date = response.xpath('//h3[@class="profile-timeline-month-heading bg-white d-inline-block h6 pr-2 py-1"]')

        # using first index to get latest contribution
        month = date[0].xpath('./text()').extract_first().strip()
        year = date[0].xpath('./span[@class="text-gray"]/text()').extract_first().strip()

        yield{
            # extracting display name
            'name': response.xpath('//span[@class="p-name vcard-fullname d-block"]/text()').extract_first(),
            # extracting src attribute of profile image
            'pic_url': response.xpath('//img[@class="avatar width-full rounded-2"]/@src').extract_first(),
            'latest_contrib_date': month + ', ' + year
        }
