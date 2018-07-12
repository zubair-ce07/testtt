import argparse
import asyncio
import time

from urllib.parse import urlparse
import validators

from concurrent_spider import RecursiveConcurrentSpider


def validate_url(url):
    if not validators.url(url):
        raise argparse.ArgumentTypeError(f"The url: {url} is not valid")
    return url


def validate_positive_input(value):
    value = float(value)
    if value < 0:
        raise argparse.ArgumentTypeError(f"The value: {value} should be greater than zero")
    return value


def parse_user_cli_arguments():
    user_command_parser = argparse.ArgumentParser()

    user_command_parser.add_argument("site_to_crawl", help="This arg stores the link of the site on "
                                                           "which crawling will be performed", type=validate_url)
    user_command_parser.add_argument("total_urls", help="This arg stores the total number of urls "
                                                        "that should be visited", type=validate_positive_input)
    user_command_parser.add_argument("download_delay", help="This arg stores the amount of delay "
                                                            "in consecutive downloads", type=validate_positive_input)
    user_command_parser.add_argument("tasks_limit", help="This arg stores the total number of task that can be "
                                                         "executed concurrently", type=validate_positive_input)

    return user_command_parser.parse_args()


def main(user_cli_args, c_spider):
    loop = asyncio.get_event_loop()
    try:
        start_time = time.time()
        loop.run_until_complete(c_spider.start_crawler([urlparse(c_spider.site_to_crawl)],
                                                       int(user_cli_args.total_urls)))
    finally:
        loop.close()

    print(f"\nTotal Requests: {c_spider.spider_execution_report.total_requests}\n"
          f"Bytes Downloaded: {c_spider.spider_execution_report.bytes_downloaded}\n"
          f"Size Per Page: "
          f"{c_spider.spider_execution_report.bytes_downloaded/c_spider.spider_execution_report.total_requests}")

    print("Execution Time: {}".format(time.time()-start_time))


if __name__ == '__main__':
    user_cli_args = parse_user_cli_arguments()
    concurrent_spider = RecursiveConcurrentSpider(user_cli_args.site_to_crawl,
                                                  user_cli_args.download_delay,
                                                  int(user_cli_args.tasks_limit))
    main(user_cli_args, concurrent_spider)
