import logging

from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.mail import MailSender

logger = logging.getLogger("email-logger")


class StatusMailer(object):

    def __init__(self, item_count, recipients, mailer):
        self.item_count = item_count
        self.items_scraped = 0
        self.recipients = recipients
        self.mailer = mailer

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 500)
        recipients = crawler.settings.getlist('STATUSMAILER_RECIPIENTS')
        mailer = MailSender.from_settings(crawler.settings)

        mailer_extension = cls(item_count, recipients, mailer)
        crawler.signals.connect(mailer_extension.send_mail, signal=signals.item_scraped)

        return mailer_extension

    def send_mail(self, item, response, spider):
        self.items_scraped += 1

        if self.items_scraped % self.item_count == 0:
            logger.info(f"Scraped {self.items_scraped} items")

            body = f"Spider ({spider.name}) has scraped {self.items_scraped} items"

            return self.mailer.send(
                to=self.recipients, body=body,
                subject=f"Spider ({spider.name}) statistics")
