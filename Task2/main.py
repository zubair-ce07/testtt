import time
import concurrent_spider
import argparse
import validators
from urllib.parse import urlparse
import asyncio


def validate_url(url):
    if not validators.url(url):
        raise argparse.ArgumentTypeError(f"The url: {url} is not valid")
    return url


def validate_input_limit(value):
    if float(value) < 0:
        raise argparse.ArgumentTypeError(f"The value: {value} should be greater than zero")
    return float(value)


user_command_parser = argparse.ArgumentParser()

user_command_parser.add_argument("site_url", help="This arg stores the link of the site on "
                                                  "which crawling will be performed", type=validate_url)
user_command_parser.add_argument("total_urls", help="This arg stores the total number of urls that should be visited",
                                 type=validate_input_limit)
user_command_parser.add_argument("download_delay", help="This arg stores the amount of delay in consecutive downloads",
                                 type=validate_input_limit)
user_command_parser.add_argument("tasks_limit", help="This arg stores the total number of task "
                                                     "that can be executed concurrently", type=validate_input_limit)

user_cli_args = user_command_parser.parse_args()
start_time = time.time()
c_spider = concurrent_spider.RecursiveConcurrentSpider(user_cli_args.site_url)

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(c_spider.start_crawler([urlparse(c_spider.site)],
                                                   int(user_cli_args.total_urls),
                                                   int(user_cli_args.download_delay),
                                                   int(user_cli_args.tasks_limit)))
finally:
    loop.close()

print(f"\nTotal Requests: {c_spider.report.total_requests}\n"
      f"Bytes Downloaded: {c_spider.report.bytes_downloaded}\n"
      f"Size Per Page: {c_spider.report.bytes_downloaded/c_spider.report.total_requests}")

print("Execution Time: {}".format(time.time()-start_time))
