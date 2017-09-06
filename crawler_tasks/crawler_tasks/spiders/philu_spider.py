import json
import re
from itertools import dropwhile

from scrapy import Selector
from scrapy.http import Request
from w3lib.url import add_or_replace_parameter, url_query_parameter

from crawler_tasks.items import PhiluCourse
from .philu_base import BaseSpider, clean, _course_id


class PhiluSpider(BaseSpider):
    name = 'philu'

    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler_tasks.pipelines.PhiluItemPipeline': 1,
            'crawler_tasks.pipelines.PhiluFilePipeline': 2,
        },
        'FILES_STORE': 'philu_files',
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_DIR': 'httpcache',
        'HTTPCACHE_STORAGE': 'scrapy.extensions.httpcache.FilesystemCacheStorage',
        'RETRY_TIMES': 1,
        'DOWNLOAD_TIMEOUT': 9999999999
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

    def strip_text_items(self, items):
        return [i.strip() for i in items if i.strip()]

    def start_crawl(self, response):
        for url in self.courses:
            yield Request(url, callback=self.parse_course)

    def parse_course(self, response):
        course = PhiluCourse()
        course['course_id'] = _course_id(response.url)
        course['lectures'] = []
        course['project'] = []
        course['assignments'] = []
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
            self.request_exercises(response)

        ]
        course['meta'] = {
            'request_queue': request_queue
        }
        return self.next_request_or_course(course)

    def parse_course_champs(self, response):
        course = response.meta['course']
        course['course_champions'] = course_champions = {'champs': {}}
        xpath = '//*[contains(@class, "lecture-page-component")][1]//text()'
        course_champions['text'] = clean(response.xpath(xpath))

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
            course['course_champions']['champs'].update({name: champ})
        return self.next_request_or_course(course)

    def parse_course_info(self, response):
        course = response.meta['course']
        faqs = {'title': clean(response.css('.full-padding::text'))[0], 'faqs': []}
        for faq_s in response.css('.lecture-page-component .span12'):
            question = {}
            for f_s in faq_s.xpath('.//p[contains(., "Q. ")] | .//p[contains(., "A. ")] | .//div[h3] | .//p'):
                text = " ".join(clean(f_s.css(' ::text')))
                if "Q. " in text:
                    question = {}
                    question['question'] = text

                elif "A. " in text:
                    question['answer'] = text
                    question['answer_html'] = f_s.extract()
                    faq['questions'] += [question]
                    question = {}

                elif f_s.xpath('.//h3'):
                    faq = {}
                    faqs['faqs'] += [faq]
                    faq['title'] = clean(f_s.css(' h3::text'))[0]
                    faq['info'] = []
                    faq['questions'] = []
                elif clean(text):
                    faq['info'] += [clean(text)]

        course['faqs'] = faqs
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
        return Request(url, headers=self.headers_with_cookies, callback=self.parse_instructor_message)

    def request_exercises(self, response):
        url = response.url.replace('/home', '/exercises/featureable_exercises.json')
        return Request(url, headers=self.headers_with_cookies, meta=response.meta, callback=self.parse_exercises)

    def request_submissions(self, response, exercise):
        url = response.url.replace('/exercises/featureable_exercises.json', '/reports/all/')
        reqs = []
        for ex in exercise:
            ex_url = url + str(ex) + '?order=trending&page=1&query='
            reqs += [Request(ex_url, headers=self.headers_with_cookies,
                             meta=response.meta, callback=self.parse_submission)]

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
        return Request(url, headers=self.headers_with_cookies,
                       meta=response.meta, callback=self.parse_submission)

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

        xpath = '//*[contains(@class, "lecture-page-navigation") and contains(., "Final Project")]//@href'
        project_urls = clean(response.xpath(xpath))
        for project_url in project_urls:
            url = response.urljoin(project_url)
            # url = 'https://philanthropyuniversity.novoed.com/capacity-2016-4/lecture_pages/844796'
            module_requests.append(
                Request(url, callback=self.parse_course_project, dont_filter=True)
            )
            # break
        champ_url = response.xpath('//a[contains(., "Meet Your Course Champions")]//@href').extract_first()
        info_url = response.xpath('//a[contains(., "Frequently Asked Questions")]//@href').extract_first()
        info_url = info_url or response.xpath('//a[contains(., "FAQs")]//@href').extract_first()
        if champ_url:
            module_requests.append(
                Request(response.urljoin(champ_url), callback=self.parse_course_champs, dont_filter=True)
            )

        if info_url:
            module_requests.append(
                Request(response.urljoin(info_url), callback=self.parse_course_info, dont_filter=True)
            )

        course = response.meta['course']
        course['course_info'] = sum((clean(l.css('li ::text')) for l in response.css('.lecture-page-navigation')[1:]),
                                    [])
        course['course_info'] = [c for c in course['course_info'] if c != 'Course Information' and c != 'New Section']
        c_in = [c for c in dropwhile(lambda x: x != 'Course Overview', course['course_info'])]
        course['course_info'] = c_in or [c for c in
                                         dropwhile(lambda x: x != 'How to Form a Team', course['course_info'])]
        course['meta']['request_queue'] += module_requests
        return self.next_request_or_course(course)

    def parse_course_project(self, response):
        selector = response.css('#lecture-components-list')
        nodes = selector.css(
            '[href^="#step"], a[href*="soundcloud"], img[src],'
            '[class=muted], [class="title-video-text"],'
            ':not(h2):not([class="muted"]):not([href^="#step"])::text,'
            '[href*=".pdf"], [href*="#attached-file"], [href], [src*="youtube"]'
        )
        module = self.parse_html_nodes(nodes, selector, response)

        course = response.meta['course']
        course['project'].append(module)

        module_index = course['project'].index(module)
        course['meta']['request_queue'] += \
            self.module_transcript_requests(module, module_index, is_project=True)

        image_url = module.get('module_image')
        if image_url:
            meta = {
                'module_index': module_index,
                'is_project': True
            }
            course['meta']['request_queue'] += [
                # a course will not be scrapped if its module
                # image gets filtered by duplicate request filter.
                Request(image_url, meta=meta, dont_filter=True,
                        callback=self.redirected_module_img_url)
            ]

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
        if response.meta.get('is_project', False):
            course['project'][module_index]['module_image'] = response.url
        else:
            course['lectures'][module_index]['module_image'] = response.url
        return self.next_request_or_course(course)

    def module_transcript_requests(self, module, module_index, is_project=False):
        transcript_requests = []
        for unit_index, unit in enumerate(module['units']):
            for video_index, video in enumerate(unit['unit_video']):
                url = video['transcript']
                meta = {
                    'module_index': module_index,
                    'unit_index': unit_index,
                    'video_index': video_index,
                    'is_project': is_project,
                }
                transcript_requests.append(
                    Request(url, meta=meta, callback=self.redirected_module_transcript_url, dont_filter=True)
                )

        return transcript_requests

    def redirected_module_transcript_url(self, response):
        course = response.meta['course']
        module_index = response.meta['module_index']
        unit_index = response.meta['unit_index']
        video_index = response.meta['video_index']
        if response.meta.get('is_project', False):
            units = course['project'][module_index]['units']
        else:
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
