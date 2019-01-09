# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_splash import SplashRequest, SlotPolicy
import base64

from scrapy.shell import open_in_browser, inspect_response




script = r'''
function main(splash, args)
    assert(splash:go(args.url))
    assert(splash:wait(5))

    splash:runjs("document.querySelector('[href*=\"comment_track\"]').click();")
    splash:runjs("window.scrollTo(0,document.body.scrollHeight);")
    splash:wait(10)

      return {
        html = splash:html(),
        png = splash:png(),
    }
end
'''


class FacebookSpiderSpider(scrapy.Spider):
    name = 'facebook_spider'

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
        "SPLASH_URL": 'http://0.0.0.0:8050/',
        "DOWNLOADER_MIDDLEWARES" : {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
        },
        "SPIDER_MIDDLEWARES" : {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        "DUPEFILTER_CLASS" : 'scrapy_splash.SplashAwareDupeFilter',
        "HTTPCACHE_STORAGE": 'scrapy_splash.SplashAwareFSCacheStorage',
        'DOWNLOAD_DELAY': 1,
        'DOWNLOAD_TIMEOUT': 60,
        'DNS_TIMEOUT': 60,
        'CONCURRENT_REQUESTS': 1
    }
    start_urls = [#
    'https://www.facebook.com/HaloTop/posts/',
    # 'https://www.facebook.com/pg/Valkyrie-Brewing-Company-328598723841647/posts/',
    # 'https://www.facebook.com/pg/Lewis-Circle-of-Horses-LLC-172603192788791/posts/'
    ]

    
    def parse(self, response):
        splash_args = {
            'wait': 0.5,
            'timeout': 60,
            'lua_source': script
        }
        posts = response.css(".userContentWrapper")
        page_id = response.css("meta[property='al:ios:url']::attr(content)").re_first(r'id?=(\d+)')

        for post in posts:
            post_id = post.css("[name='ft_ent_identifier']::attr(value)").extract_first()
            post_time = post.xpath("descendant-or-self::*[@class='timestampContent']/../@title").extract()
            message = post.xpath("descendant-or-self::*[@data-ad-preview='message']"
                                    "[contains(@class,'userContent')]//text()").extract()
            name = post.css('.fwb a::text').extract()[0]
            image_url = post.css(".uiScaledImageContainer img::attr(src)").extract()
            post_data = {
                "page_id": page_id,
                "url": "{}{}".format(response.url, post_id),
                "id": post_id,
                "created_time": post_time,
                "message": "".join(message),
                "name": name,
                "picture": image_url
            }
            yield SplashRequest(post_data['url'], self.parse_post, endpoint='execute',
                            args=splash_args, slot_policy=SlotPolicy.SINGLE_SLOT)


    def parse_post(self, response):
        name = response.url.split('/')[-1] + '.png'
        with open(name, 'wb') as f:
            f.write(base64.b64decode(response.data['png']))

        response = scrapy.http.HtmlResponse(url='converted response ', body=response.data['html'], encoding='utf-8')

        post_data = {
            'likes_count': response.css('[href*="comment_tracking"] span:contains(Likes)::text').re_first(r'\d+'),
            'comments_count': response.css('[href*="comment_tracking"] span:contains(Comments)::text').re_first(r'\d+'),
            'share_count': response.css('[href*="comment_tracking"] span:contains(Shares)::text').re_first(r'\d+'),
            'comments': []
        }

        for comment in response.css(".UFIComment"):
             post_data["comments"].append({
                "actor_name": comment.css(".UFICommentActorName::text").extract_first(),
                "comment_body": "".join(comment.css(".UFICommentBody ::text").extract())
            })

        yield post_data
        # inspect_response(response, self)
        # open_in_browser(response)
