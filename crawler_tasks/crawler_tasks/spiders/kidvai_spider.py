
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawler_tasks.items import KidvaiPost


class KidvaiSpider(CrawlSpider):
    name = 'kidvai'
    allowed_domains = ['kidvai.blogspot.com', 'blogger.com']
    start_urls = ['http://kidvai.blogspot.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy.pipelines.files.FilesPipeline': 1,
        },
        'FILES_STORE': 'kidvai_images'
    }
    rules = (
        Rule(LinkExtractor(allow=('archive\.html',)), callback='parse_blog_page'),
    )

    def parse_start_url(self, response):
        return self.parse_blog_page(response)

    def parse_blog_page(self, response):
        for post in response.css('.post'):
            yield self.parse_post(post)

    def parse_post(self, post):
        kidvai_post = KidvaiPost()
        kidvai_post['name_id'] = post.css('a::attr(name)').extract_first()
        kidvai_post['title'] = post.css('.post-title::text').extract_first()

        body = post.css('.post-body')
        kidvai_post['body_text'] = body.extract_first()
        kidvai_post['file_urls'] = body.css('.post-body img::attr(src)').extract()
        kidvai_post['labels'] = body.css('.blogger-labels a::text').extract()

        footer = post.css('.post-footer')
        kidvai_post['url'] = footer.css('a[title="permanent link"]::attr(href)').extract_first()
        kidvai_post['posted_by'] = footer.css('em::text').extract_first()
        kidvai_post['posted_time'] = footer.css('em a::text').extract_first()
        comment_count = footer.css('.comment-link::text').re('(\d+)')
        if comment_count and int(comment_count[0]):
            comments_link = footer.css('.comment-link::attr(href)').extract_first()
            return Request(comments_link, callback=self.parse_comments,
                           meta={'kidvai_post': kidvai_post, 'dont_obey_robotstxt': True})
        else:
            kidvai_post['comments'] = []
            return kidvai_post

    def parse_comments(self, response):
        comments_block = response.css('#comments')
        user_names = comments_block.css('#comments-block dt a::text').extract()
        user_urls = comments_block.css('#comments-block dt a::attr(href)').extract()
        comment_text = comments_block.css('#comments-block dd').extract()
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
