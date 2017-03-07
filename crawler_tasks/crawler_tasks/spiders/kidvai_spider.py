
from scrapy import Spider
from scrapy.http import Request
from crawler_tasks.items import KidvaiPost


class KidvaiSpider(Spider):
    name = 'kidvai'
    allowed_domains = ['kidvai.blogspot.com', 'blogger.com']
    start_urls = ['http://kidvai.blogspot.com/']

    def parse(self, response):
        archive_links = response.css('ul.archive-list a::attr(href)').extract()
        for link in archive_links:
            yield Request(link, callback=self.parse_blog_page)
        return self.parse_blog_page(response)

    def parse_blog_page(self, response):
        for post in response.css('div.post'):
            yield self.parse_post(post)

    def parse_post(self, post):
        kidvai_post = KidvaiPost()
        kidvai_post['name_id'] = post.css('a::attr(name)').extract_first()
        kidvai_post['title'] = post.css('h3.post-title::text').extract_first()

        body = post.css('div.post-body')
        kidvai_post['body_text'] = body.extract_first()
        kidvai_post['file_urls'] = body.css('div.post-body img::attr(src)').extract()
        kidvai_post['labels'] = body.css('p.blogger-labels a::text').extract()

        footer = post.css('p.post-footer')
        kidvai_post['url'] = footer.css('em a[title="permanent link"]::attr(href)').extract_first()
        kidvai_post['posted_by'] = footer.css('em::text').extract_first()
        kidvai_post['posted_time'] = footer.css('em a::text').extract_first()
        comment_count = footer.css('a.comment-link::text').re('(\d+)')
        if comment_count and int(comment_count[0]):
            comments_link = footer.css('a.comment-link::attr(href)').extract_first()
            return Request(comments_link, callback=self.parse_comments,
                           meta={'kidvai_post': kidvai_post, 'dont_obey_robotstxt': True})
        else:
            kidvai_post['comments'] = []
            return kidvai_post

    def parse_comments(self, response):
        comments_block = response.css('div#comments')
        user_names = comments_block.css('dl#comments-block dt a::text').extract()
        user_urls = comments_block.css('dl#comments-block dt a::attr(href)').extract()
        comment_text = comments_block.css('dl#comments-block dd').extract()
        comments = []
        for comment in list(zip(user_names, user_urls, comment_text)):
            comments.append({
                'user_name': comment[0],
                'profile_url': comment[1],
                'text': comment[2]
            })

        kidvai_post = response.meta['kidvai_post']
        kidvai_post['comments'] = comments
        return kidvai_post
