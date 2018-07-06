import time
import concurrent_spider
import argparse

user_command_parser = argparse.ArgumentParser()

user_command_parser.add_argument("site_url", help="This arg stores the link of the site on "
                                                  "which crawling will be performed", type=str)
user_command_parser.add_argument("total_urls", help="This arg stores the total number of urls that should be visited",
                                 type=int)
user_command_parser.add_argument("download_delay", help="This arg stores the amount of delay in consecutive downloads",
                                 type=float)
user_command_parser.add_argument("tasks_limit", help="This arg stores the total number of task "
                                                     "that can be executed concurrently", type=int)

user_cli_args = user_command_parser.parse_args()

start_time = time.time()
c_spider = concurrent_spider.RecursiveConcurrentSpider(user_cli_args.site_url)
c_spider.run_crawler(user_cli_args.total_urls, user_cli_args.download_delay, user_cli_args.tasks_limit)

print(f"\nTotal Requests: {c_spider.report.total_requests}\n"
      f"Bytes Downloaded: {c_spider.report.bytes_downloaded}\n"
      f"Size Per Page: {c_spider.report.bytes_downloaded/c_spider.report.total_requests}")

print("Execution Time: {}".format(time.time()-start_time))
