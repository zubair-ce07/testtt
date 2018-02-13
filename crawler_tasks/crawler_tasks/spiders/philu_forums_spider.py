import json

from scrapy import Selector
from scrapy.http import Request
from w3lib.url import add_or_replace_parameter, url_query_cleaner

from crawler_tasks.items import PhiluProgram
from .philu_base import BaseSpider, clean, _course_id


class PhiluSpider(BaseSpider):
    name = 'philu-forums'

    custom_settings = {
        'ITEM_PIPELINES': {
            # 'crawler_tasks.pipelines.PhiluItemPipeline': 1,
            # 'crawler_tasks.pipelines.PhiluFilePipeline': 2,
        },
        'FILES_STORE': 'philu_files',
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_DIR': 'httpcache',
        'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage',
        'RETRY_TIMES': 1,
        'DOWNLOAD_TIMEOUT': 9999999999
    }

    pdf_url_t = '{}attachments/{}/view'

    def start_crawl(self, response):
        url = 'https://philanthropyuniversity.novoed.com/philanthropy-initiative/oe/#!/home'
        yield Request(url, meta={'is_program': True}, callback=self.parse_program)

        for url in self.courses:
            yield Request(url, meta={'is_program': False}, callback=self.parse_program)

    def parse_program(self, response):
        program = PhiluProgram()
        program['url'] = response.url
        is_program = response.meta['is_program']
        program['is_program'] = is_program
        if is_program:
            name = clean(response.css('.head-part ::text'))[0]
        else:
            name = clean(response.css('.program-breadcrumbs a:not([href])::text'))[0]

        program['course_title'] = name
        program['course_id'] = _course_id(response.url)
        program['discussions'] = {}
        program['discussion_likes'] = {}
        program['post_likes'] = {}
        program['course_roles'] = {}
        requests = [self.request_discussions(response),
                    self.request_forums(response),
                    self.request_course_roles(response)]

        program['meta'] = {'request_queue': requests}
        return self.next_request_or_program(program)

    def parse_course_roles(self, response):
        program = response.meta['program']
        program['course_roles'] = json.loads(response.text)['result']
        return self.next_request_or_program(program)

    def parse_forum(self, response):
        program = response.meta['program']
        program['forums'] = json.loads(response.text)['result']
        return self.next_request_or_program(program)

    def parse_discussion_likes(self, response):
        d_id = response.meta['did']
        program = response.meta['program']
        program['discussion_likes'][d_id] = json.loads(response.text)['result']
        return self.next_request_or_program(program)

    def parse_discussions(self, response):
        program = response.meta['program']
        disc = json.loads(response.text)['result']
        if not disc:
            return self.next_request_or_program(program)

        for d_id, dis in disc.items():
            sel = Selector(text=dis['body'])
            dis['image_urls'] = []
            program['meta']['request_queue'] += self.request_redirected_discussion_img_url(sel, d_id)
            if dis['num_posts']:
                program['meta']['request_queue'] += [self.request_posts(response, d_id)]

            if dis['num_likes']:
                program['meta']['request_queue'] += [self.request_discussion_likes(response, d_id)]

        program['discussions'].update(disc)

        min_weight = min([d['trending_weight'] for d in disc.values()])
        filt_disc = [k for k, d in disc.items() if min_weight == d['trending_weight'] and not d['highlighted']]
        filt_disc = filt_disc or [k for k, d in disc.items() if min_weight == d['trending_weight']]
        min_key = min(filt_disc or [20])
        program['meta']['request_queue'] += [self.request_discussions(response, min_key)]
        return self.next_request_or_program(program)

    def parse_post_likes(self, response):
        p_id = response.meta['pid']
        program = response.meta['program']
        program['post_likes'][p_id] = json.loads(response.text)['result']
        return self.next_request_or_program(program)

    def parse_posts(self, response):
        program = response.meta['program']
        did = response.meta['id']
        raw_posts = json.loads(response.text)['result']
        discussion = program['discussions'][did]
        posts = raw_posts['posts']
        if 'created_at' not in response.url and 'posts' in discussion:
            return self.next_request_or_program(program)

        if 'posts' not in discussion:
            discussion['posts'] = []

        discussion['posts'] += posts
        if posts:
            program['meta']['request_queue'] += [self.request_next_posts(response, did, raw_posts)]

        for post in posts:
            if post['num_likes']:
                program['meta']['request_queue'] += [self.request_post_likes(response, post['id'])]

            if not post['comments_count']:
                continue

            if post['comments_count'] > len(post.get('comments', [])):
                program['meta']['request_queue'] += [self.request_comments(response, did, post)]

        return self.next_request_or_program(program)

    def parse_comments(self, response):
        program = response.meta['program']
        did = response.meta['did']
        pid = response.meta['pid']
        discussion = program['discussions'][did]
        post = [p for p in discussion['posts'] if p['id'] == pid][0]
        raw_comments = json.loads(response.text)
        post['comments'].update({c['id']: c for c in raw_comments['comments']})
        if raw_comments['count'] > len(post['comments']):
            program['meta']['request_queue'] += \
                [self.request_next_comments(response, raw_comments, did, pid)]
        return self.next_request_or_program(program)

    def request_next_posts(self, response, did, posts):
        url = url_query_cleaner(response.url)
        url = url + "?before_id={}&order=created_at".format(posts['first_post_id'])
        return Request(url, headers=self.headers_with_cookies, meta={'id': did},
                       callback=self.parse_posts, dont_filter=True)

    def request_comments(self, response, did, post):
        last_comment = min([c for c in post['comments']])
        url = url_query_cleaner(response.url).split('/topics')[0]
        url = url + "/posts/{}/comments?before_id={}&order=created_at".format(post['id'], last_comment)
        return Request(url, headers=self.headers_with_cookies, meta={'did': did, 'pid': post['id']},
                       callback=self.parse_comments, dont_filter=True)

    def request_next_comments(self, response, raw_comments, did, pid):
        last_comment = min([c for c in raw_comments['comments']])
        url = url_query_cleaner(response.url)
        url = url + "?before_id={}&order=created_at".format(last_comment)

        return Request(url, headers=self.headers_with_cookies, meta={'did': did, 'pid': pid},
                       callback=self.parse_comments, dont_filter=True)

    def request_redirected_discussion_img_url(self, sel, d_id):
        req = []
        for url in sel.css('img::attr(src)').extract():
            if 'fbcdn' in url:
                continue
            req += [Request(url, self.redirected_discussion_img_url, method='HEAD',
                            meta={'id': d_id, 'handle_httpstatus_list': [403]}, dont_filter=True)]

        return req

    def redirected_discussion_img_url(self, response):
        program = response.meta['program']
        did = response.meta['id']
        program['discussions'][did]['image_urls'] += [response.url]
        program['discussions'][did]['image_urls'] = list(set(program['discussions'][did]['image_urls']))
        return self.next_request_or_program(program)

    def request_discussion_likes(self, response, did):
        url_t = 'https://philanthropyuniversity.novoed.com/{}/topics/{}/voters?page=1'
        url = url_t.format(_course_id(response.url), did)
        return Request(url, headers=self.headers_with_cookies, meta={'did': did},
                       callback=self.parse_discussion_likes, dont_filter=True)

    def request_posts(self, response, did):
        url = url_query_cleaner(response.url) + '/' + str(did) + '/posts'
        return Request(url, headers=self.headers_with_cookies, meta={'id': did},
                       callback=self.parse_posts, dont_filter=True)

    def request_post_likes(self, response, pid):
        url_t = 'https://philanthropyuniversity.novoed.com/{}/posts/{}/voters?page=1'
        url = url_t.format(_course_id(response.url), pid)
        return Request(url, headers=self.headers_with_cookies, meta={'pid': pid},
                       callback=self.parse_post_likes, dont_filter=True)

    def request_forums(self, response):
        course_id = _course_id(response.url)
        url = 'https://philanthropyuniversity.novoed.com/{}/forums'.format(course_id)
        return Request(url, headers=self.headers_with_cookies,
                       meta={'dont_cache': True}, callback=self.parse_forum)

    def request_discussions(self, response, last_topic=''):
        if '/topics' in response.url:
            url = add_or_replace_parameter(response.url, 'last_topic_id', last_topic)
        else:
            course_id = _course_id(response.url)
            url = 'https://philanthropyuniversity.novoed.com/{}/topics?order=trending_weight'.format(course_id)

        return Request(url, headers=self.headers_with_cookies, callback=self.parse_discussions)

    def request_course_roles(self, response):
        url_t = "https://philanthropyuniversity.novoed.com/{}/course_roles"
        url = url_t.format(_course_id(response.url))
        return Request(url, headers=self.headers_with_cookies, callback=self.parse_course_roles)

    def next_request_or_program(self, program):
        request_queue = program['meta']['request_queue']
        if request_queue:
            request = request_queue.pop()
            request.meta['program'] = program
            request.priority = 1
            return request

        del program['meta']
        return program
