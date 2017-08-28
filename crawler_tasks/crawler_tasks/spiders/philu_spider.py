import re
import json
from urllib.parse import unquote

from scrapy import Selector
from scrapy.selector import XPathSelector
from scrapy.spiders import Spider
from scrapy.http import Request
from w3lib.url import add_or_replace_parameter, url_query_parameter, url_query_cleaner

from crawler_tasks.items import PhiluCourse


def _sanitize(input_val):
    """ Shorthand for sanitizing results, removing unicode whitespace and normalizing end result"""
    if isinstance(input_val, XPathSelector):
        # caller obviously wants clean extracted version
        to_clean = input_val.extract()
    else:
        to_clean = input_val

    return re.sub('\s+', ' ', to_clean.replace('\xa0', ' ')).strip()


def clean(lst_or_str):
    """ Shorthand for sanitizing results in an iterable, dropping ones which would end empty """
    if not isinstance(lst_or_str, str) and getattr(lst_or_str, '__iter__', False):  # if iterable and not a string like
        return [x for x in (_sanitize(y) for y in lst_or_str if y is not None) if x]
    return _sanitize(lst_or_str)


class PhiluSpider(Spider):
    name = 'philu'
    allowed_domains = [
        'novoed.com', 'cloudfront.net',
        'philanthropyuniversity.novoed.com'
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler_tasks.pipelines.PhiluItemPipeline': 1,
            'crawler_tasks.pipelines.PhiluFilePipeline': 2,
        },
        'FILES_STORE': 'philu_files',
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_DIR': 'httpcache',
        'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage',
        'RETRY_TIMES': 1
    }

    pdf_url_t = '{}attachments/{}/view'

    def new_course_module(self):
        return {
            'units': [],
            'module_description': [],
            'toc_list': []
        }

    def new_module_unit(self):
        return {
            'unit_audio': [],
            'unit_video': [],
            'unit_content': [],
            'unit_pdf': [],
            'unit_links': []
        }

    def csrf_token(self, response):
        for cookie in response.headers.getlist('Set-Cookie'):
            match = re.match('XSRF-TOKEN=(.*);', cookie.decode())
            if match:
                return unquote(match.group(1))

    def strip_text_items(self, items):
        return [i.strip() for i in items if i.strip()]

    def __init__(self):
        super().__init__()
        self.email = 'muhammad.zeeshan@arbisoft.com'
        self.password = 'CfR-c9C-Jh8-B7o'

    def start_requests(self):
        url = 'https://app.novoed.com/my_account.json'
        meta = {
            'handle_httpstatus_list': [401],
            'dont_cache': True
        }
        return [Request(url, callback=self.sign_in_request, meta=meta)]

    def sign_in_request(self, response):
        payload = {
            'user': {
                'email': self.email,
                'password': self.password
            },
            'catalog_id': 'philanthropy-initiative'
        }
        url = 'https://app.novoed.com/users/sign_in.json'
        headers = {
            'Content-Type': 'application/json;charset=utf-8',
            'X-XSRF-TOKEN': self.csrf_token(response),
            'dont_cache': True
        }
        return Request(
            url, callback=self.request_home_page, method='POST',
            body=json.dumps(payload), headers=headers)

    def request_home_page(self, response):
        url = 'https://philanthropyuniversity.novoed.com/philanthropy-initiative/oe/#!/home'
        meta = {
            'sign_in_response': response
        }
        return Request(url, meta=meta, callback=self.courses_menu)

    def courses_menu(self, response):
        urls = ['https://philanthropyuniversity.novoed.com/capacity-2016-4/home',
                'https://philanthropyuniversity.novoed.com/scale-2017-1/home',
                'https://philanthropyuniversity.novoed.com/entrepreneurship-2017-1/home',
                'https://philanthropyuniversity.novoed.com/strategy-2017-1/home',
                'https://philanthropyuniversity.novoed.com/financial-modeling-2017-1/home',
                'https://philanthropyuniversity.novoed.com/leadership-2017-1/home',
                'https://philanthropyuniversity.novoed.com/fundraising-2017-1/home',
                'https://philanthropyuniversity.novoed.com/fundraising-2017-2/home'
                ]
        course_urls = response.css('.courses_menu ::attr(href)').extract()
        for url in course_urls:
            yield Request(urls[7], meta=response.meta, callback=self.parse_course)
            return

    def parse_course(self, response):
        # return
        course = PhiluCourse()
        course['lectures'] = []
        course['assignments'] = []
        course['discussions'] = {}
        course['url'] = response.url
        course['course_title'] = response.css(
            '.program-breadcrumbs a:not([href])::text'
        ).extract_first().strip()

        raw_text = response.css(
            '.onboarding-expandable ::attr("compile-once")'
        ).extract_first()
        selector = Selector(text=raw_text, type='html')

        course['course_welcome_text'] = self.strip_text_items(
            selector.css('::text').extract()
        )
        course['course_welcome_raw_html'] = selector.extract()
        course['course_welcome_youtube_video'] = selector.css('[src*="youtube"]::attr(src)').extract_first()
        course['course_champions'] = {}
        course['course_info'] = {}

        course_img_url = selector.css('::attr(src)').extract_first()
        request_queue = [
            Request(course_img_url, callback=self.redirected_course_img_url),
            self.request_lectures_section(response),
            self.request_assignments_section(response),
            self.request_course_announcements(response),
            self.request_forums(response),
            self.request_discussions(response),
            self.request_exercises(response)

        ]
        course['meta'] = {
            'request_queue': request_queue
        }
        return self.next_request_or_course(course)

    def parse_forum(self, response):
        course = response.meta['course']
        course['forums'] = json.loads(response.text)['result']
        return self.next_request_or_course(course)

    def parse_discussions(self, response):
        course = response.meta['course']
        disc = json.loads(response.text)['result']
        if disc:
            for d_id, dis in disc.items():
                sel = Selector(text=dis['body'])
                dis['image_urls'] = []
                course['meta']['request_queue'] += self.request_redirected_discussion_img_url(sel, d_id)
                if not dis['num_posts']:
                    continue
                course['meta']['request_queue'] += [self.request_discussion_comments(response, d_id)]

            course['discussions'].update(disc)

            min_weight = min([d['trending_weight'] for d in disc.values()])
            filt_disc = [k for k, d in disc.items() if min_weight == d['trending_weight'] and not d['highlighted']]
            filt_disc = filt_disc or [k for k, d in disc.items() if min_weight == d['trending_weight']]
            min_key = min(filt_disc or [20])
            course['meta']['request_queue'] += [self.request_discussions(response, min_key)]
        return self.next_request_or_course(course)

    def parse_course_champs(self, response):
        course = response.meta['course']
        for champ_s in response.css('.table.table-bordered td'):
            champ = {}
            name = champ_s.css('a ::attr(alt)').extract_first()
            if not name:
                continue

            champ['name'] = name
            champ['url'] = champ_s.css('a ::attr(href)').extract_first()
            champ['img'] = champ_s.css('a ::attr(src)').extract_first()
            champ['from'] = clean(champ_s.css('::text'))[-2]
            champ['post'] = clean(champ_s.css('::text'))[-1]
            course['course_champions'].update({name: champ})
        return self.next_request_or_course(course)

    def parse_course_info(self, response):
        course = response.meta['course']
        faqs = []
        for faq_s in response.css('.lecture-page-component .span12'):
            faq = {}
            faqs += [faq]
            faq['title'] = clean(faq_s.css('div h3::text'))[0]
            faq['questions'] = []
            for q_s, a_s in zip(faq_s.xpath('.//p[contains(., "Q. ")]'), faq_s.xpath('.//p[contains(., "A. ")]')):
                question = {}
                question['question'] = clean(q_s.css(' ::text'))[0]
                question['answer'] = clean(a_s.css(' ::text'))[0]
                question['answer_html'] = a_s.extract()
                faq['questions'] += [question]

        course['faqs'] = faqs
        return self.next_request_or_course(course)

    def parse_discussion_comments(self, response):
        course = response.meta['course']
        did = response.meta['id']
        posts = json.loads(response.text)['result']['posts']
        course['discussions'][did]['posts'] = posts
        return self.next_request_or_course(course)

    def parse_exercises(self, response):
        course = response.meta['course']
        exercises = json.loads(response.text)['result']
        course['exercises'] = exercises
        course['meta']['request_queue'] += self.request_submissions(response, exercises)
        return self.next_request_or_course(course)

    def parse_submission(self, response):
        course = response.meta['course']
        exercise_num = re.findall('all/(\d*)', response.url)[0]
        submissions = json.loads(response.text)['result']
        if not submissions:
            return self.next_request_or_course(course)

        exercise = course['exercises'][exercise_num]
        if 'submissions' not in exercise:
            exercise['submissions'] = {}

        exercise['submissions'].update({s['id'].split('_')[-1]: s for s in submissions})
        course['meta']['request_queue'] += [self.request_next_submissions(response)]
        course['meta']['request_queue'] += self.request_submission_urls(response, submissions)
        course['meta']['request_queue'] += self.request_report_comments(response, submissions)
        return self.next_request_or_course(course)

    def parse_submission_url(self, response):
        course = response.meta['course']
        url = response.xpath("//a[contains(., 'Download original file')]//@href").extract_first()
        xpath = "//div[*[contains(., 'Download original file')] and h4[@class='thick-border']]/h4"
        report_num = re.findall('reports/(\d*)', response.url)[0]
        for e_id, exercise in course['exercises'].items():
            if 'submissions' not in exercise:
                continue
            submission = exercise['submissions'].get(report_num)
            if not submission:
                continue

            submission['file_url'] = url
            submission['image_urls'] = []
            submission['content'] = response.xpath('//div[*[contains(@id, "sec-")]]').extract()
            submission['content'] += response.xpath(xpath).extract()
            for c in submission['content']:
                sel = Selector(text=c)
                course['meta']['request_queue'] += self.request_redirected_submission_img_url(sel, e_id, report_num)
            break

        return self.next_request_or_course(course)

    def parse_report_comment(self, response):
        course = response.meta['course']
        comments = json.loads(response.text)

        report_num = re.findall('reports/(\d*)', response.url)[0]
        for exercise in course['exercises'].values():
            if 'submissions' not in exercise:
                continue
            submission = exercise['submissions'].get(report_num)
            if not submission:
                continue
            if isinstance(comments, list):
                submission['comments'] += comments
            else:
                submission['comments'] = comments['comments']
            if len(submission['comments']) < submission['comments_count']:
                course['meta']['request_queue'] += [self.request_report_next_comments(response, submission)]
            break

        return self.next_request_or_course(course)

    def request_redirected_submission_img_url(self, sel, e_id, report_num):
        req = []
        for url in sel.css('img::attr(src)').extract():
            if not url or 'mail.google' in url or 'fbcdn' in url:
                continue

            req += [Request(url, self.redirected_submission_img_url,
                            meta={'eid': e_id, 'report_num': report_num,
                                  'handle_httpstatus_list': [403]}, dont_filter=True)]

        return req

    def request_redirected_discussion_img_url(self, sel, d_id):
        req = []
        for url in sel.css('img::attr(src)').extract():
            req += [Request(url, self.redirected_discussion_img_url, meta={'id': d_id}, dont_filter=True)]

        return req

    def redirected_discussion_img_url(self, response):
        course = response.meta['course']
        did = response.meta['id']
        course['discussions'][did]['image_urls'] += [response.url]
        course['discussions'][did]['image_urls'] = list(set(course['discussions'][did]['image_urls']))
        return self.next_request_or_course(course)

    def redirected_submission_img_url(self, response):
        course = response.meta['course']
        if response.status == 403:
            return self.next_request_or_course(course)

        eid = response.meta['eid']
        sid = response.meta['report_num']
        course['exercises'][eid]['submissions'][sid]['image_urls'] += [response.url]
        course['exercises'][eid]['submissions'][sid]['image_urls'] = list(
            set(course['exercises'][eid]['submissions'][sid]['image_urls']))
        return self.next_request_or_course(course)

    def redirected_course_img_url(self, response):
        course = response.meta['course']
        course['course_image'] = response.url
        return self.next_request_or_course(course)

    def request_lectures_section(self, response):
        lectures_section_url = \
            response.css('.lectures ::attr(href)').extract_first()
        url = response.urljoin(lectures_section_url)
        return Request(url, callback=self.request_course_modules)

    def request_assignments_section(self, response):
        assignment_section_url = \
            response.css('.assignments ::attr(href)').extract_first()
        url = response.urljoin(assignment_section_url)
        return Request(url, callback=self.request_course_assignments)

    def request_course_announcements(self, response):
        url = response.urljoin('announcements')
        sign_in_response = response.meta['sign_in_response']
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/plain, */*',
            'X-CSRF-TOKEN': self.csrf_token(sign_in_response)
        }
        return Request(url, headers=headers, callback=self.parse_instructor_message)

    def request_discussion_comments(self, response, did):
        url = url_query_cleaner(response.url) + '/' + str(did) + '/posts'
        sign_in_response = response.meta['sign_in_response']
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/plain, */*',
            'X-CSRF-TOKEN': self.csrf_token(sign_in_response)
        }
        return Request(url, headers=headers, meta={'id': did}, callback=self.parse_discussion_comments,
                       dont_filter=True)

    def request_forums(self, response):
        url = response.url.replace('/home', '/forums')
        sign_in_response = response.meta['sign_in_response']
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/plain, */*',
            'X-CSRF-TOKEN': self.csrf_token(sign_in_response)
        }
        return Request(url, headers=headers, callback=self.parse_forum)

    def request_discussions(self, response, last_topic=''):
        if '/topics' in response.url:
            url = add_or_replace_parameter(response.url, 'last_topic_id', last_topic)
        else:
            url = response.url.replace('/home', '/topics?order=trending_weight')
        sign_in_response = response.meta['sign_in_response']
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/plain, */*',
            'X-CSRF-TOKEN': self.csrf_token(sign_in_response)
        }
        return Request(url, headers=headers, meta=response.meta, callback=self.parse_discussions)

    def request_exercises(self, response):
        url = response.url.replace('/home', '/exercises/featureable_exercises.json')
        sign_in_response = response.meta['sign_in_response']
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/plain, */*',
            'X-CSRF-TOKEN': self.csrf_token(sign_in_response)
        }
        return Request(url, headers=headers, meta=response.meta, callback=self.parse_exercises)

    def request_submissions(self, response, exercise):
        url = response.url.replace('/exercises/featureable_exercises.json', '/reports/all/')
        reqs = []
        for ex in exercise:
            ex_url = url + str(ex) + '?order=trending&page=1&query='
            sign_in_response = response.meta['sign_in_response']
            headers = {
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json, text/plain, */*',
                'X-CSRF-TOKEN': self.csrf_token(sign_in_response)
            }
            reqs += [Request(ex_url, headers=headers, meta=response.meta, callback=self.parse_submission)]

        return reqs

    def request_submission_urls(self, response, submissions):
        reqs = []
        for submission in submissions:
            url = submission['url']
            reqs += [Request(url, meta=response.meta, callback=self.parse_submission_url, dont_filter=True)]
        return reqs

    def request_report_comments(self, response, submissions):
        reqs = []
        for submission in submissions:
            if submission['comments_count']:
                reqs += [Request(submission['url'] + '/comments',
                                 meta=response.meta, callback=self.parse_report_comment)]

        return reqs

    def request_report_next_comments(self, response, submission):
        url = response.url
        if 'more_before' not in url:
            url += '/more_before'
        last_id = min([c['id'] for c in submission['comments']])
        url = add_or_replace_parameter(url, 'last_comment_id', str(last_id))
        return Request(url, self.parse_report_comment, meta=response.meta)

    def request_next_submissions(self, response):
        page = int(url_query_parameter(response.url, 'page'))
        url = add_or_replace_parameter(response.url, 'page', page + 1)
        sign_in_response = response.meta['sign_in_response']
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json, text/plain, */*',
            'X-CSRF-TOKEN': self.csrf_token(sign_in_response)
        }
        return Request(url, headers=headers, meta=response.meta, callback=self.parse_submission)

    def request_course_modules(self, response):
        module_urls = response.css('.lecture-page-navigation')[0] \
            .css('::attr(href)').extract()

        module_requests = []
        for module_url in module_urls:
            url = response.urljoin(module_url)
            # url = 'https://philanthropyuniversity.novoed.com/capacity-2016-4/lecture_pages/844796'
            module_requests.append(
                Request(url, callback=self.parse_course_module, dont_filter=True)
            )
            # break
        champ_url = response.xpath('//a[contains(., "Meet Your Course Champions")]//@href').extract_first()
        info_url = response.xpath('//a[contains(., "Frequently Asked Questions")]//@href').extract_first()
        if champ_url:
            module_requests.append(
                Request(response.urljoin(champ_url), callback=self.parse_course_champs, dont_filter=True)
            )

        if champ_url:
            module_requests.append(
                Request(response.urljoin(info_url), callback=self.parse_course_info, dont_filter=True)
            )

        course = response.meta['course']
        info_x = '//*[contains(@class, "lecture-page-navigation") and contains(., "Course Information")]/li//text()'
        course['course_info'] = clean(response.xpath(info_x))[1:]
        course['meta']['request_queue'] += module_requests
        return self.next_request_or_course(course)

    def parse_course_module(self, response):
        selector = response.css('#lecture-components-list')
        nodes = selector.css(
            '[href^="#step"], a[href*="soundcloud"], img[src],'
            '[class=muted], [class="title-video-text"],'
            ':not(h2):not([class="muted"]):not([href^="#step"])::text,'
            '[href*=".pdf"], [href*="#attached-file"], [href], [src*="youtube"]'
        )
        module = self.parse_html_nodes(nodes, selector, response)

        course = response.meta['course']
        course['lectures'].append(module)

        module_index = course['lectures'].index(module)
        course['meta']['request_queue'] += \
            self.module_transcript_requests(module, module_index)

        image_url = module.get('module_image')
        if image_url:
            meta = {
                'module_index': module_index
            }
            course['meta']['request_queue'] += [
                # a course will not be scrapped if its module
                # image gets filtered by duplicate request filter.
                Request(image_url, meta=meta, dont_filter=True,
                        callback=self.redirected_module_img_url)
            ]

        return self.next_request_or_course(course)

    def redirected_module_img_url(self, response):
        course = response.meta['course']
        module_index = response.meta['module_index']
        course['lectures'][module_index]['module_image'] = response.url
        return self.next_request_or_course(course)

    def module_transcript_requests(self, module, module_index):
        transcript_requests = []
        for unit_index, unit in enumerate(module['units']):
            for video_index, video in enumerate(unit['unit_video']):
                url = video['transcript']
                meta = {
                    'module_index': module_index,
                    'unit_index': unit_index,
                    'video_index': video_index,
                }
                transcript_requests.append(
                    Request(url, meta=meta, callback=self.redirected_module_transcript_url)
                )

        return transcript_requests

    def redirected_module_transcript_url(self, response):
        course = response.meta['course']
        module_index = response.meta['module_index']
        unit_index = response.meta['unit_index']
        video_index = response.meta['video_index']

        units = course['lectures'][module_index]['units']
        video = units[unit_index]['unit_video'][video_index]
        video['transcript'] = response.url

        return self.next_request_or_course(course)

    def module_title(self, response, selector):
        title = selector.css('h2::text').extract_first()
        if not title:
            return response.css('h2::text').extract_first()
        return title

    def parse_html_nodes(self, nodes, selector, response):
        module = self.new_course_module()
        module['module_title'] = self.module_title(response, selector)

        unit = None
        module_desc_complete = False
        for node in nodes:
            text = node.extract().strip()
            if not text or re.match('\$\(', text):
                continue

            if (self.node_is_toc_title(node, module)
                or self.node_is_audio_link(node, unit)
                or self.node_is_pdf_link(response.url, node, unit)
                or self.node_is_an_image(node, module, unit, module_desc_complete)
                or self.node_is_a_video(node, unit, selector)
                or self.node_is_a_link(node, unit)
                ):
                pass

            elif self.node_is_unit_title(node, module, unit):
                unit = self.new_module_unit()
                unit['unit_title'] = text

            elif self.node_is_toc_item(node, module):
                module_desc_complete = True

            elif not module_desc_complete:
                module['module_description'].append(text)

            elif not node.css('[href*=".pdf"], [href*="#attached-file"]'):
                unit['unit_content'].append(text)

        # append last unit to module, if any
        if unit:
            module['units'].append(unit)

        return module

    def node_is_toc_title(self, node, module):
        if node.css('[class="muted"]'):
            module['toc_title'] = node.css('::text').extract()
            return True

    def node_is_audio_link(self, node, unit):
        if node.css('a[href*="soundcloud"]'):
            unit['unit_audio'].append(
                node.css('::attr(href)').extract_first()
            )
            return True

    def node_is_a_link(self, node, unit):
        if node.re('Step \d+:'):
            return False

        if not unit:
            return False

        if node.css('[href], [src*="youtube"]'):
            link = {node.css('::text').extract_first(): node.css('::attr(href), ::attr(src)').extract_first()}
            unit['unit_links'] += [link]
            return True

    def node_is_pdf_link(self, parent_url, node, unit):
        if node.css('a[href*=".pdf"]'):
            node_text = node.css(' ::text').extract_first()
            if not node_text:
                return
            unit['unit_pdf'].append(
                {node_text: node.css('::attr(href)').extract_first()}
            )
            # unit['unit_content'] += [node_text]
            return True

        if node.css('[href*="#attached-file"]'):
            course_url = parent_url.split('lecture_pages')[0]
            file_name = node.css('::attr(href)').extract_first()
            file_url = self.pdf_url_t.format(course_url, file_name.split('-')[-1])
            node_text = node.css(' ::text').extract_first()
            unit['unit_pdf'].append(
                {node_text: file_url}
            )
            # unit['unit_content'] += [node_text]
            return True

    def node_is_an_image(self, node, module, unit, module_desc_complete):
        if node.css('img[src]'):
            image_url = node.css('::attr(src)').extract_first()
            if 'ajax-loader' in image_url:
                return True

            if not module_desc_complete:
                module['module_image'] = image_url
            elif not node.css('[class="lecture-video-thumb"]'):
                unit['unit_image'] = image_url
            return True

    def node_is_a_video(self, node, unit, selector):
        if node.css('[class="title-video-text"]'):
            video_name = node.css('::text').extract_first().strip()
            video_id = node.css('::attr(id)').re('\d+')[0]

            elem_css = '[id="video-download-link-{}"]::attr(href)'.format(video_id)
            video_url = selector.css(elem_css).extract_first()

            elem_css = '[id="transcript-link-{}"]::attr(href)'.format(video_id)
            transcript_url = selector.css(elem_css).extract_first()

            unit['unit_video'].append({
                'name': video_name,
                'url': video_url,
                'transcript': transcript_url
            })
            return True

    def node_is_unit_title(self, node, module, unit):
        if node.re('Step \d+:'):
            if unit:
                module['units'].append(unit)
            return True

    def node_is_toc_item(self, node, module):
        if node.css('[href^="#step"]'):
            module['toc_list'].append(
                node.css('::text').extract()
            )
            return True

    def request_course_assignments(self, response):
        assignment_urls = response.css('.exercise-table ::attr(href)').extract()

        assignment_requests = []
        for assignment_url in assignment_urls:
            url = response.urljoin(assignment_url)
            assignment_id = re.search('\d+$', assignment_url).group()
            elem_css = '[id="exercise-{}-title"]::text'.format(assignment_id)
            meta = {
                'assignment_title': response.css(elem_css).extract_first().strip()
            }
            assignment_requests.append(
                Request(url, meta=meta, callback=self.parse_course_assignment)
            )

        course = response.meta['course']
        course['meta']['request_queue'] += assignment_requests
        return self.next_request_or_course(course)

    def parse_course_assignment(self, response):
        raw_text = response.css('.expandable ::attr(compile-once)').extract_first()
        if not raw_text:
            raw_text = response.css('.expandable').extract_first()

        selector = Selector(text=raw_text, type='html')
        content = selector.css('::text').extract()
        content = self.strip_text_items(content)
        raw_html = selector.extract()

        course = response.meta['course']
        assignment = {
            'raw_html': raw_html,
            'url': response.url,
            'assignment_title': response.meta['assignment_title'],
            'assignment_content': content
        }
        attachments = {}
        files_s = response.css(".span6[id*='attachment-']")
        for f_s in files_s:
            link = f_s.css("a[data-no-turbolink]:not([data-toggle])::attr(href)").extract_first()
            name = f_s.css("[data-no-turbolink][data-toggle]::text").extract_first()
            attachments.update({name: link})

        dropbox_links = {}

        files_s = response.css("[href*='dropbox']")
        for f_s in files_s:
            link = f_s.css("::attr(href)").extract_first()
            name = f_s.css(" ::text").extract_first()
            dropbox_links.update({name: link})

        assignment['attachments'] = attachments
        assignment['dropbpox_links'] = dropbox_links
        course['assignments'].append(assignment)
        return self.next_request_or_course(course)

    def parse_instructor_message(self, response):
        result = json.loads(response.text)['result'][0]
        sel = Selector(text=result['description'], type='html')
        texts = sel.css('::text').extract()

        course = response.meta['course']
        course['instructor_msg_title'] = result['title']
        course['instructor_msg_content'] = self.strip_text_items(texts)
        course['instructor_msg_html'] = sel.extract()
        return self.next_request_or_course(course)

    def next_request_or_course(self, course):
        request_queue = course['meta']['request_queue']
        if request_queue:
            request = request_queue.pop()
            request.meta['course'] = course
            request.priority = 1
            return request

        del course['meta']
        return course
