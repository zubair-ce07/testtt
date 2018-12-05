# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.shell import inspect_response
from scrapy_splash import SplashRequest, SlotPolicy

lua_script = """
function main(splash)
    splash:wait(3)
    assert(splash:go(splash.args.url))
    return splash:html()
end
"""

class FacebookNewSpider(scrapy.Spider):
    name = 'facebook_new'
    allowed_domains = ['facebook.com']
    # start_urls = ['http://facebook.com/']

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
        'DOWNLOAD_DELAY': 5,
        'DOWNLOAD_TIMEOUT': 60,
        'DNS_TIMEOUT': 60,
        # 'CONCURRENT_REQUESTS': 1
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
            'lua_source': lua_script
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
            yield SplashRequest(post_data['url'], meta={'item': post_data}
                            , callback=self.parse_splash_respone, endpoint='execute',
                            args=splash_args, slot_policy=SlotPolicy.SINGLE_SLOT)


    def parse_splash_respone(self, response):
        text = response.text
        cookies = re.findall(r'"(_js[^"]+)","([^"]+)",', text)
        cookies = {c[0]: c[1] for c in cookies}

        lsd = re.findall(r'"LSD",\[\],\{"token":"([^"]+)"', text)
        if not cookies or not lsd:
            self.logger.error("Missing cookies or parameters: %s",
                              response.url)
            return
        lsd = lsd[0]

        ft_ent_identifier = response.xpath('//body').re_first(r'name="ft_ent_identifier"\s+value="([^"]+)"')
        if not ft_ent_identifier:
            self.logger.error("Missing ft_ent_identifier: ")
            return
        
        item = response.meta['item']
        item['like_count'] = response.xpath('//script//text()').re_first('likecount:(\d+)')
        item['comment_count'] = response.xpath('//script//text()').re_first('commentcount:(\d+)')
        item['share_count'] = response.xpath('//script//text()').re_first('sharecount:(\d+)')

        headers = {
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {}
        data['__user'] = '0'
        data['__a'] = '1'
        data['lsd'] = lsd

        meta = {
            'lsd': lsd,
            'x_cookies': cookies,
            'item': item,
            'ft_ent_identifier': ft_ent_identifier,
        }
        return scrapy.FormRequest(
            'https://www.facebook.com/cookie/consent/?dpr=1',
            headers=headers,
            formdata=data,
            cookies=cookies,
            callback=self.parse_cookie_consent,
            meta=meta,
            dont_filter=True,
        )

    def parse_cookie_consent(self, response):
        ft_ent_identifier = response.meta['ft_ent_identifier']
        data = {'ft_ent_identifier': ft_ent_identifier}

        data['viewas'] = ''
        data['source'] = '2'
        data['offset'] = '1'
        data['length'] = '2'
        data['orderingmode'] = 'ranked_threaded'
        data['section'] = 'default'

        data['feed_context'] = ('{"is_viewer_page_admin":false,"is_notification_preview":false,'
                                '"autoplay_with_channelview_or_snowlift":false,"video_player_origin"'
                                ':"permalink","fbfeed_context":true,"location_type":5,'
                                '"outer_object_element_id":"u_0_p","object_element_id":'
                                '"u_0_p","is_ad_preview":false,"is_editable":false,'
                                '"mall_how_many_post_comments":2,"bump_reason":0,"enable_comment":'
                                'false,"story_width":502,"tn-str":"-R"}')

        data['numpagerclicks'] = ''
        data['av'] = ''

        data['__user'] = '0'
        data['__a'] = '1'
        data['__req'] = '4'
        data['__be'] = '-1'
        data['__pc'] = 'PHASED:DEFAULT'
        data['__rev'] = '4323872'
        data['lsd'] = response.meta['lsd']

        cookies = {'datr': response.meta['x_cookies']['_js_datr']}

        meta = {
            'lsd': response.meta['lsd'],
            'x_cookies': response.meta['x_cookies'],
            'item': response.meta['item'],
            'ft_ent_identifier': ft_ent_identifier,
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Authority': 'www.facebook.com',
            'Origin': 'www.facebook.com',
        }

        return scrapy.FormRequest(
            'https://www.facebook.com/ajax/ufi/comment_fetch.php?dpr=1',
            formdata=data,
            headers=headers,
            cookies=cookies,
            callback=self.parse_comments,
            meta=meta,
        )

    def parse_comments(self, response):
        try:
            text = response.text.replace('for (;;);', '')
            obj = json.loads(text)

        except Exception:
            self.logger.exception("Error getting the posts from %s",
                                  response.url)
            return

        comments = obj['jsmods']['require'][0][3][1]

        all_comments = []

        for c in comments['comments']:
            all_comments.append({
                'comment_body': c['body']['text'],
                'actor_name': comments['profiles'][c['author']]['name']
            })

        item = response.meta['item']
        item['comments'] = all_comments

        yield item    
