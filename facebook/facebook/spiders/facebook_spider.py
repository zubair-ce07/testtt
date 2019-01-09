# -*- coding: utf-8 -*-
import csv
import re

import scrapy


class FacebookSpiderSpider(scrapy.Spider):
    name = 'facebook'
    allowed_domains = ['facebook.com']
    start_urls = [
        'https://www.facebook.com/pg/32199396998/',
        'https://www.facebook.com/pg/305269616200809/',
        'https://www.facebook.com/pg/254329181245659/',
        'https://www.facebook.com/pg/41102509388/',
    ]

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
        'DOWNLOAD_DELAY': 2,
        'COOKIES_ENABLED': False
    }

    def start_requests(self):
        with open('fb.csv') as f:
            d = csv.DictReader(f)
            for df in d:
                yield scrapy.Request('https://www.facebook.com/pg/{}/'.format(df['fb_id']))
                break

    def parse(self, response):
        fields = {
            'name': response.css('#seo_h1_tag span::text').extract_first(),
            'id': self.pick_first(
                response.css('[property="al:android:url"]::attr(content)').re(r'\d+')),
            'talking_about_count': response.css('[name="description"]::attr(content)').re_first(
                r'([\d,])\s*talking\s*about\s*this'),
            'were_here_count': response.css('[name="description"]::attr(content)').re_first(
                r'([\d,])\s*were\s*here'),
            'overall_star_rating': response.xpath(
                '//*[contains(text(), "out of 5")]/text()').re_first(r'[\d\.]+'),
            'engagement': {
                'like_count': response.xpath(
                    '//*[contains(text(), "people like this")]/text()').re_first(r'[\d,]+'),
                'social_sentence': response.xpath(
                    '//*[contains(text(), "people follow this")]/text()').re_first(r'[\d,]+')
            },
            'fan_count': response.xpath(
                '//*[contains(text(), "people like this")]/text()').re_first(r'[\d,]+'),
            'link': response.url,
        }

        request = response.follow('./about', callback=self.parse_about)
        request.meta['fields'] = fields
        return request

    def parse_about(self, response):
        fields = {
            'price_range': response.xpath(
                '//*[text()="Price range"]/following::div[1]//*/text()').extract_first(),
            'food_style': response.xpath(
                '//*[text()="Cuisine"]/following::span[1]/text()').extract(),
            'restaurant_specialties': response.xpath(
                '//*[text()="Specialties"]/following::span[1]/text()').extract(),
            'company_overview': ''.join(response.xpath(
                '//*[text()="Company Overview"]/following::div[1]/text()').extract()),
            'phone': self.pick_first(
                response.xpath('//div[contains(text(), "Call")]').re(r'\+[\- 0-9]+')),
            'emails': response.css('[href^="mailto"] div::text').extract(),
            'about': ''.join(response.xpath(
                '//*[contains(text(), "MORE INFO")]/following::*[contains(text(), "About")][1]'
                '/following::div[1]/text()').extract()),
            'category': response.css('[href*="/search"]::text').extract_first(),
            'category_list': response.css('[href*="/search"]::text').extract(),
            'location': ''.join(response.xpath(
                '//*[@src="https://static.xx.fbcdn.net/rsrc.php/v3/yS/r/QeKYFue6x0O.png"]'
                '/following::div[1]//*/text()').extract()),
            'start_info': {}
        }

        start_type, start_date = self.fetch_start_info(response.xpath(
            '//*[@src="https://static.xx.fbcdn.net/rsrc.php/v3/yZ/r/Qz1rawS_hSy.png"]'
            '/following::div[1]//*/text()').extract_first())
        fields['start_info']['type'] = start_type
        fields['start_info']['date'] = start_date

        fields['founded'] = response.xpath(
            '//*[@src="https://static.xx.fbcdn.net/rsrc.php/v3/yZ/r/Qz1rawS_hSy.png"]/'
            'following::div[1]//*/text()').re_first(r'\d\d\d\d')
        r = response.xpath('//*[contains(text(), "Mission")]/following::div[1]')
        fields['mission'] = ''.join(r.css(
            '.text_exposed_root::text, .text_exposed_show::text').extract())
        r = response.xpath('//div[contains(text(), "Products")]')
        fields['products'] = ''.join(r.css(
            'div + div .text_exposed_root::text, div + div .text_exposed_show::text').extract())
        r = response.xpath('//*[text()="General Information"]/following::div[1]')
        fields['general_info'] = ''.join(r.css(
            '.text_exposed_root::text, .text_exposed_show::text').extract())
        fields.update(response.meta['fields'])

        request = response.follow('./reviews', callback=self.parse_reviews)
        request.meta['fields'] = fields
        return request

    def parse_reviews(self, response):
        fields = {
            'rating_count': response.xpath(
                '//*[contains(text(), "Based on the opinion of")]/text()').re_first(r'[\d,]+')
        }

        fields.update(response.meta['fields'])

        request = response.follow('./posts', callback=self.parse_posts)
        request.meta['fields'] = fields
        return request

    @staticmethod
    def parse_posts(response):
        posts = []
        raw_posts = response.css(".userContentWrapper")
        page_id = response.css("meta[property='al:ios:url']::attr(content)").re_first(r'id?=(\d+)')
        for post in raw_posts:
            post_id = post.css("[name='ft_ent_identifier']::attr(value)").extract_first()
            post_time = post.xpath(
                "descendant-or-self::*[@class='timestampContent']/../@title").extract_first()
            message = post.xpath("descendant-or-self::*[@data-ad-preview='message']"
                                 "[contains(@class,'userContent')]//text()").extract()
            name = post.css('.fwb a::text').extract()[0]
            image_url = post.css(".uiScaledImageContainer img::attr(src)").extract_first()
            posts.append({
                "url": "{}/{}".format(response.url, post_id),
                "id": post_id,
                "created_time": post_time,
                "message": "".join(message),
                "name": name,
                "picture": image_url
            })

        return {
            'fb_data': response.meta['fields'],
            'fb_id': page_id,
            'fb_posts': posts
        }

    @staticmethod
    def pick_first(value):
        if value:
            return value[0]

        return

    def fetch_start_info(self, value):
        if not value:
            return None, None

        if 'in' in value:
            s = value.split('in')
        elif 'on' in value:
            s = value.split('on')
        else:
            return None, None

        s_type = s[0].strip()
        s_month = self.pick_first(re.findall(r'[A-Za-z]+', s[1]))
        s_nums = [int(n) for n in re.findall(r'\d+', s[1])]
        
        if len(s_nums) > 1:
            s_day = min(s_nums)
            s_year = max(s_nums)
        elif len(s_nums) == 1:
            s_year = s_nums[0]
            s_day = None
        else:
            s_year = None
            s_day = None

        return s_type, {'day': s_day, 'year': s_year, 'month': s_month}
