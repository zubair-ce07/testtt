from items import FellowshipLoader
from scrapy.http import FormRequest
from urlparse import urljoin
import datetime
import scrapy
import time

class ProFellowSpider(scrapy.Spider):
    name = "profellow_spider"
    start_urls = [
        'https://www.profellow.com/profile/login/',
    ]

    def parse(self, response):
        unique_id = response.xpath('//input[@id="unique_id"]/@value').extract_first()
        nonce = response.xpath('//input[@id="_myuserpro_nonce"]/@value')\
            .extract_first()
        form_data = {
                '{}{}'.format('force_redirect_uri-', unique_id): '0',
                '{}{}'.format('redirect_uri-', unique_id): '',
                '_myuserpro_nonce': nonce,
                'unique_id': unique_id,
                '{}{}'.format('username_or_email-', unique_id): 'rabiaalam',
                '{}{}'.format('user_pass-', unique_id): 'l!f3isbeautiful',
                'action': 'userpro_process_form',
                'template': 'login',
        }

        return FormRequest(
            url="https://www.profellow.com/wp-admin/admin-ajax.php",
            formdata=form_data,
            callback=self.on_login)

    def on_login(self, response):
        yield scrapy.Request('https://www.profellow.com/wp-admin'
                             '/admin-ajax.php?action=elastic_filter&type%5B%5D'
                             '=professional', self.after_login)

    def after_login(self, response):
        for href in response.xpath('//h2/a/@href').extract():
            yield scrapy.Request(urljoin('https://www.profellow.com', href)
                                 , self.parse_fellowship)

    def parse_fellowship(self, response):
        fellowship = FellowshipLoader(selector=response)
        time_now = datetime.datetime.now().fromtimestamp(time.time())\
            .strftime('%Y-%m-%d %H:%M:%S.%f')
        fellowship.add_value('crawled_at', time_now)
        fellowship.add_xpath('deadline', '//span[@class="_start"]/text()')
        fellowship.add_xpath('description', '//div[@class="entry-content"]//text()')
        fellowship.add_xpath('disciplines', '//div[@id="fellowship-discipline"]/text()[2]')
        fellowship.add_xpath('experience', '//div[@id="fellowship-details"]/ul'
                                           '/li[2]/text()')
        fellowship.add_xpath('external_id', '//a[@href="#"]/@data-postid')
        fellowship.add_xpath('fellowship_organization','//h2[@class="fellowship-organization"]/text()')
        fellowship.add_xpath('fellowship_url', '//a[@class="btn btn-apply"]'
                                               '/@href')
        fellowship.add_xpath('keywords', '//div[@id="fellowship-keywords"]/text()[2]')
        fellowship.add_xpath('location', '//div[@id="fellowship-details"]/ul'
                                         '/li[3]/text()')
        fellowship.add_value('provider', 'profellow')
        fellowship.add_xpath('site_record_url', '//link[@rel="canonical"]'
                                                '/@href')
        fellowship.add_xpath('title', '//h1/text()')
        return fellowship.load_item()

