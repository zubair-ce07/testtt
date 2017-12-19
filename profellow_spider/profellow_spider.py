from items import Fellowship
from scrapy.http import FormRequest
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, TakeFirst
import datetime
import scrapy
import time

class ProFellowSpider(scrapy.Spider):
    name = "profellow_spider"
    start_urls = [
        'https://www.profellow.com/profile/login/',
    ]

    def parse(self, response):
        id = response.xpath('//input[@id="unique_id"]/@value').extract_first()
        nonce = response.xpath('//input[@id="_myuserpro_nonce"]/@value')\
            .extract_first()
        form_data = {
                'force_redirect_uri-' + id: '0',
                'redirect_uri-' + id: '',
                '_myuserpro_nonce': nonce,
                'unique_id': id,
                'username_or_email-' + id: 'rabiaalam',
                'user_pass-' + id: 'l!f3isbeautiful',
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
            yield response.follow(href, self.parse_fellowship)

    def parse_fellowship(self, response):
        fellowship = ItemLoader(item=Fellowship(), response=response)
        fellowship.default_output_processor = TakeFirst()
        time_now = datetime.datetime.now().fromtimestamp(time.time())\
            .strftime('%Y-%m-%d %H:%M:%S.%f')
        fellowship.add_value('crawled_at', time_now)
        fellowship.add_xpath('deadline', '//span[@class="_start"]/text()')
        description = "".join(response.xpath('//div[@class="entry-content"]'
                                             '//text()').extract()).strip()
        fellowship.add_value('description', description)
        disciplines = response.xpath('//div[@id="fellowship-discipline"]'
                                     '/text()[2]').extract_first()\
            .replace(" ", "").split(",")
        fellowship.disciplines_out = Compose()
        fellowship.add_value('disciplines', disciplines)
        fellowship.add_xpath('experience', '//div[@id="fellowship-details"]/ul'
                                           '/li[2]/text()')
        fellowship.add_xpath('external_id', '//a[@href="#"]/@data-postid')
        fellowship_organization = response.xpath('//h2[@class="fellowship'
                                                 '-organization"]/text()')\
            .extract_first().lstrip().rstrip()
        fellowship.add_value('fellowship_organization',
                             fellowship_organization)
        fellowship.add_xpath('fellowship_url', '//a[@class="btn btn-apply"]'
                                               '/@href')
        keywords = response.xpath('//div[@id="fellowship-keywords"]'
                                  '/text()[2]').extract_first()\
            .replace(" ", "").replace("\n", "").split(",")
        fellowship.keywords_out = Compose()
        fellowship.add_value('keywords', keywords)
        fellowship.add_xpath('location', '//div[@id="fellowship-details"]/ul'
                                         '/li[3]/text()')
        fellowship.add_value('provider', 'profellow')
        fellowship.add_xpath('site_record_url', '//link[@rel="canonical"]'
                                                '/@href')
        fellowship.add_xpath('title', '//h1/text()')
        return fellowship.load_item()

