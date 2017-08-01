from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging

from django.db import DatabaseError
from scrapy.exceptions import DropItem
from sumy.nlp.stemmers import Stemmer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.utils import get_stop_words

from news.models import News, NewsSource
from categories.models import Category

def logger_configuration():
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


class NewsScrappersPipeline(object):
    LANGUAGE = "english"
    SENTENCES_COUNT = 5
    logger = logger_configuration()

    def process_item(self, item, spider):
        error_message = '{} : {}'
        try:
            category, created = Category.objects.get_or_create(name=item.get('category','un-identified').lower())
            news_source, created = NewsSource.objects.get_or_create(name=item.get('news_source', 'un-identified').lower())
            News.objects.update_or_create(title=item['title'],
                                          source_url=item['source_url'],
                                          image_url=item['image_url'],
                                          abstract=item['abstract'],
                                          detail=item['detail'],
                                          summary=self.get_summary(item['detail']),
                                          published_date=item['published_date'],
                                          newspaper=spider.getNewspaper(),
                                          category=category,
                                          news_source=news_source
                                          )
            return item

        except DatabaseError as e:
            self.logger.error(error_message.format(spider.name,str(e)))
            raise DropItem()
        except KeyError as e:
            self.logger.error(error_message.format(spider.name,str(e)))
            raise DropItem()
        except Exception as e:
            self.logger.exception(error_message.format(spider.name,str(e)))
            raise DropItem()

    def get_summary(self, text):
        parser = PlaintextParser.from_string(text, Tokenizer(self.LANGUAGE))
        stemmer = Stemmer(self.LANGUAGE)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(self.LANGUAGE)
        summary = [str(sentence) for sentence in summarizer(parser.document, self.SENTENCES_COUNT)]
        return ' '.join(summary)
