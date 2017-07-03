from django.db import models
from url_crawler.utils import URLSpider


class WebPage(models.Model):
    url = models.URLField()
    # size of the page in bytes
    size_of_page = models.PositiveIntegerField()
    tags_count = models.PositiveIntegerField()
    meta_tags_count = models.PositiveIntegerField()
    links_count = models.PositiveIntegerField()

    def __str__(self):
        return self.url

    @classmethod
    def get_or_create(cls, url):
        """
        Checks if url is already visited and data is in database
        if not visits url and saves to database and returns the result

        Arguments:
            url (str): url against which to search
        Returns:
            page (WebPage()): content of the web page at given url
        """
        page_set = cls.objects.filter(url=url)

        # not found in the database
        if not page_set.exists():
            spider = URLSpider(url)
            results = spider.crawl()

            # Tried to visit url but failed due to invalid url
            if results is None:
                page = None
            else:
                page = cls.objects.create(
                    url=url,
                    size_of_page=results['size'],
                    tags_count=results['tags_count'],
                    meta_tags_count=results['meta_tags'],
                    links_count=len(results['links'])
                )

                # storing all links on the page to database
                Link.objects.bulk_create(
                    [Link(url=link_url, web_page=page) for link_url in results['links']]
                )

        # found in database
        else:
            # saving first in queryset
            page = page_set.first()

        return page


class Link(models.Model):
    web_page = models.ForeignKey(WebPage, on_delete=models.CASCADE)
    # address in href attribute in links on page
    url = models.URLField(max_length=500)
