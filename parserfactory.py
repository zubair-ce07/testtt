from webcrawlerasync import WebCrawlerAsync
from webcrawlerconcurrent import WebCrawlerConcurrent
from webcrawlerbasic import WebCrawlerBasic


class ParserFactory:
    @staticmethod
    def get_parser(parser_type, download_delay, max_request, concurrent_request_count):
        class_alias = {
            "async": WebCrawlerAsync,
            "concurrent": WebCrawlerConcurrent,
            "basic": WebCrawlerBasic,
        }.get(parser_type)
        if not class_alias:
            class_alias = WebCrawlerBasic

        return class_alias(download_delay, max_request, concurrent_request_count)
